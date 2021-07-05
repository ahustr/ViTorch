#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/6/26 13:25
# ide： PyCharm

import os,sys
from abc import abstractmethod

from PyQt5.QtCore import pyqtSignal, QObject, QPropertyAnimation, QSize, QEventLoop, QTimer
from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog,QApplication

from mainWindow.lib.mainWindow import Ui_Form
from XThread import XThread_win
from Editor.editor_logicW import Editor_logic
from Datasets.datasets_logic import XDatasets
from Training.train import Train, device, Matplotlib_qt_figure
from torch.optim import Adam

pro_path = os.path.abspath("./").replace("\\","/")

class mainWindowFunction(Ui_Form, QWidget):
    def __init__(self):
        super(mainWindowFunction, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("ViTorch V1.0")
        self.left_bars.setMaximumWidth(0)
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        print('\n')
        self.stackedWidget.setCurrentIndex(0)
        self.left_bars.setMinimumSize(QSize(0, 0))
        self.editor_append_to_main_window()
        self.slot_init()
        self.__test_dynamic_plot()

    def editor_append_to_main_window(self):
        self.editor = Editor_logic()
        self.editor_layout.addWidget(self.editor)

    def __test_dynamic_plot(self):
        self.convas_axes = {}
        batch_figure = Matplotlib_qt_figure()
        batch_figure.fig.suptitle("batch train_val")
        batch_figure.axes1 = batch_figure.fig.add_subplot(1, 1, 1)
        batch_figure.axes1.set_title("loss")
        self.convas_axes["batch_loss"] = batch_figure
        self.chart_layout.addWidget(batch_figure)

    def __plot_on(self,epoch,xloss,yloss,xacc,yacc):
        self.update_convas(xloss,yloss,self.convas_axes["batch_loss"].axes1,self.convas_axes["batch_loss"])

    def update_convas(self,xdata,ydata,axes,figure):
        line = axes.plot(xdata,ydata)
        axes.draw_artist(axes.patch)
        axes.draw_artist(line)
        figure.fig.canvas.update()
        figure.fig.canvas.blit()
        figure.fig.flush_events()
        QApplication.processEvents()

    def slot_init(self):
        self.btn_generate.clicked.connect(self.editor.generate)
        self.tbtn_add_Activation.clicked.connect(self.editor.add_activation)
        self.tbtn_add_BatchNorm1d.clicked.connect(self.editor.add_BatchNorm1d)
        self.tbtn_add_BatchNorm2d.clicked.connect(self.editor.add_BatchNorm2d)
        self.tbtn_add_Conv.clicked.connect(self.editor.add_conv)
        self.tbtn_add_dropout.clicked.connect(self.editor.add_Dropout)
        self.tbtn_add_FlattenLayer.clicked.connect(self.editor.add_flattenlayer)
        self.tbtn_add_Linear.clicked.connect(self.editor.add_Linear)
        self.tbtn_add_Maxpool.clicked.connect(self.editor.add_pool)
        self.tbtn_makeDatasets.clicked.connect(self.__makeDatasets)
        self.btn_train.clicked.connect(self.__train)
        self.btn_train_stop.clicked.connect(self.__stop_train_thread)
        self.btn_train_stop.setEnabled(False)
        self.btn_loadDatasets.clicked.connect(self.__load_datasets)
        self.btn_loadNetMoudle.clicked.connect(self.__loadNetMoudle)
        self.btn_toggle.clicked.connect(self.menu_slide)

    def __makeDatasets(self):
        url_path = "file:///" + pro_path + "/Datasets/Xlib/html/datasets_firstdemo.html"
        self.datastesWindow = XDatasets(url_path)
        self.datastesWindow.show()

    def __train(self):
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.btn_train.setEnabled(False)
        self.btn_train_stop.setEnabled(True)
        self.train = Train()
        self.train.batch_loss.connect(self.__plot_on)
        self.train.batch_acc.connect(self.__plot_on)
        lr = float(self.doubleSpinBox_LR.text())
        num_epochs = int(self.spinBox_epoch.text())
        batch_size = int(self.spinBox_batch.text())
        exercise = int(self.spinBox_exercise.text())
        dataset_path = self.lineEdit.text()
        save = self.btn_train_save.isChecked()
        # alldata, train_iter, test_iter = self.train.load_datasets(dataset_path + "/",batch_size,resize=224)
        train_iter, test_iter = self.train.load_data_fashion_mnist(batch_size,resize=224)
        if not train_iter or not test_iter:
            QMessageBox.information(self,'ViTorch Studio failed',"当前文件夹无数据集\n（找不到'train'和'val'文件夹！）",QMessageBox.Yes)
            self.btn_train.setEnabled(True)
            self.btn_train_stop.setEnabled(False)
        else:
            if num_epochs  and batch_size  and lr:
                try:
                    optimizer = Adam(self.net.parameters(), lr=lr)
                except:
                    QMessageBox.information(self, 'ViTorch Studio failed', "当前网络模型为空！请 generate 并且 “加载模型”！",
                                            QMessageBox.Yes)
                    self.btn_train.setEnabled(True)
                    self.btn_train_stop.setEnabled(False)
                    return
                self.train_thread = XThread_win(lambda: self.train.train(self.net, train_iter, test_iter, optimizer, device, num_epochs,save))
                self.train_thread.finished.connect(self.__train_thread_finished)
                self.train_thread.start()

    def __load_datasets(self):
        filename=QFileDialog.getExistingDirectory(self, "选取文件夹", 'D:\PyCharm2020\PyTorch\PlantVillage')
        self.lineEdit.setText(filename)
        return filename

    def __loadNetMoudle(self):
        # net_path, _ = QFileDialog.getOpenFileName(self, "❄⚽选取网络模型文件（.py）", pro_path, "*.py")
        try:
            from generated.ViTorchNet import ViTorchNet,FlattenLayer
            self.net = ViTorchNet()
            print("网络模型：",self.net,sep=" ")
            return self.net
        except ModuleNotFoundError:
            QMessageBox.information(self, 'ViTorch Studio failed', "请generate网络模型！",QMessageBox.Yes)
            return

    def __stop_train_thread(self):
        self.train_thread.stopThread()
        self.btn_train.setEnabled(True)
        self.btn_train_stop.setEnabled(False)
    def __train_thread_finished(self):
        self.btn_train.setEnabled(True)
        self.btn_train_stop.setEnabled(False)
    def menu_slide(self):
        """
        左边菜单动画
        :return:
        """
        cur_width = self.left_bars.width()
        if cur_width == 0:
            end_width = 201
            self.btn_toggle.setText("收 起")
        else:
            end_width = 0
            self.btn_toggle.setText("菜 单")
        animate = QPropertyAnimation(self.left_bars, b'maximumWidth', self)
        animate.setDuration(400)
        animate.setStartValue(cur_width)
        animate.setEndValue(end_width)
        animate.start()

    def outputWritten(self, text):
        """
        捕获输出内容输出到指定的位置，这里指的是textEdit控件
        :param text: 捕获的输出内容
        :return:
        """
        cursor = self.console.textCursor()
        if text.startswith('\r'):
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        else:
            cursor.movePosition(QTextCursor.End)
        info = text.strip("\r")
        cursor.insertText(info)
        self.console.setTextCursor(cursor)
        self.console.ensureCursorVisible()

    def closeEvent(self, event):
        """
        关闭事件
        @param event:
        @return:
        """
        reply = QMessageBox.question(self,'ViTorch Studio confirm',"是否要退出 ViTorch Studio？",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit(0)
        else:
            event.ignore()

class EmittingStr(QObject):
    """
    信号捕获系统将要输出的内容，后面指定输出位置，默认是print输出到console
    """
    textWritten  = pyqtSignal(str)  # 定义一个发送str的信号
    def write(self, text):
        self.textWritten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec_()

    @abstractmethod
    def flush(self):
        pass

# if __name__ == '__main__':
#     from PyQt5.QtWidgets import QApplication
#     import cgitb,sys
#     cgitb.enable(1, None, 5, '')
#     app = QApplication(sys.argv)
#     window = mainWindowFunction()
#     window.show()
#     sys.exit(app.exec_())
