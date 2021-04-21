#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/1/13 13:50 
# ide： PyCharm

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import cv2
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from demo01 import Ui_MainWindow
from predict import Checknet
from train_ResNet import Resnet_Train

class Thread(QtCore.QThread):
    """
    重载线程QThread
    """
    signal = QtCore.pyqtSignal(str)
    draw_batch_signal = QtCore.pyqtSignal(int,list,list,list,list)
    draw_epoch_signal = QtCore.pyqtSignal(int,list,list,list,list)
    def __init__(self,fun):
        QtCore.QThread.__init__(self)
        self.fun = fun
    def run(self):
            self.fun()
    def stop(self):
        print("thread: {} quit!".format( str(self.fun)))
        self.quit()

class EmittingStr(QtCore.QObject):
    """
    信号捕获系统将要输出的内容，后面指定输出位置，默认是print输出到console
    """
    textWritten  = QtCore.pyqtSignal(str)  # 定义一个发送str的信号
    def write(self, text):
        self.textWritten.emit(str(text))

class MyFigure(FigureCanvas):
    """
    定义一个画图的接口，用于pyqt5和matplotlib的链接，即在pyqt上面显示matplotlib图像
    """
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)

class UI_logic(QtWidgets.QMainWindow):
    """
    界面的逻辑实现
    """
    thread_stop_signal = QtCore.pyqtSignal()
    def __init__(self):
        super(UI_logic, self).__init__()
        self.Ui = Ui_MainWindow()
        self.Ui.setupUi(self)
        # self.__console = sys.stdout
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

        # 相机初始化
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.timer_yolo_predict = QtCore.QTimer()
        self.camera = cv2.VideoCapture()
        self.camera_yolo_predict = cv2.VideoCapture()
        self.count = 0
        self.UI_bg_init()   #Ui界面美化设置
        self.slot_signal_init()

    def UI_bg_init(self):
        self.Ui.stackedWidget.setCurrentIndex(0)
        self.figure_batch = MyFigure(width=4, height=3, dpi=100)
        self.figure_batch.fig.suptitle("batch train_val")
        self.figure_batch.axes1 = self.figure_batch.fig.add_subplot(121)
        self.figure_batch.axes1.set_title("loss")
        self.figure_batch.axes2 = self.figure_batch.fig.add_subplot(122)
        self.figure_batch.axes2.set_title("accuracy")
        self.Ui.verticalLayout_17.addWidget(self.figure_batch)

        self.figure_epoch = MyFigure(width=5, height=4, dpi=100)
        self.figure_epoch.fig.suptitle("epoch train_val")
        self.figure_epoch.axes1 = self.figure_batch.fig.add_subplot(121)
        self.figure_epoch.axes1.set_title("loss")
        self.figure_epoch.axes2 = self.figure_batch.fig.add_subplot(122)
        self.figure_epoch.axes2.set_title("accuracy")
        self.Ui.verticalLayout_17.addWidget(self.figure_epoch)

        self.epoch = 0

    def slot_signal_init(self):
        # 界面按钮点击事件绑定
        self.Ui.pushButton_ResNet_load.clicked.connect(lambda: self.load_dataset("data_dir_ResNet"))
        self.Ui.pushButton_load_pix_path.clicked.connect(lambda: self.load_dataset("camera_pix_path"))
        self.Ui.actionopendata.triggered.connect(lambda: self.load_dataset("data_dir_ResNet"))
        self.Ui.actionResNet_2.triggered.connect(lambda: self.Ui.stackedWidget.setCurrentIndex(0))
        self.Ui.actionUNet.triggered.connect(lambda: self.Ui.stackedWidget.setCurrentIndex(1))
        self.Ui.actionmakedata.triggered.connect(lambda: self.Ui.stackedWidget.setCurrentIndex(2))
        self.Ui.actionyolov5.triggered.connect(lambda :self.Ui.stackedWidget.setCurrentIndex(3))
        self.Ui.actionyolov4.triggered.connect(lambda: self.Ui.stackedWidget.setCurrentIndex(3))
        self.Ui.actionyolov3.triggered.connect(lambda: self.Ui.stackedWidget.setCurrentIndex(3))
        self.Ui.actionquit.triggered.connect(self.close)
        self.Ui.actionquitApp.triggered.connect(self.close)
        self.Ui.actiondatabase.triggered.connect(lambda :self.Ui.stackedWidget.setCurrentIndex(2))
        self.Ui.pushButton_ResNet_train.clicked.connect(lambda: self.train_thread("ResNet"))
        self.Ui.pushButton_ResNet_cancel.clicked.connect(self.stop_train)
        self.Ui.pushButton_ResNet_predict_imgpath.clicked.connect(lambda: self.load_dataset("imgpath_ResNet"))
        self.Ui.pushButton_ResNet_predict_netpath.clicked.connect(lambda: self.load_dataset("netpath_ResNet"))
        self.Ui.pushButton.clicked.connect(lambda: self.predict("ResNet_predict"))
        self.Ui.pushButton_open_file.clicked.connect(lambda: self.camera_thread("file"))
        self.Ui.pushButton_open_camera.clicked.connect(lambda: self.camera_thread("camera"))
        self.Ui.pushButton_get_current.clicked.connect(self.btn_get_camera_pix)
        self.Ui.pushButton_4.clicked.connect(self.rootDir)
        self.Ui.pushButton_6.clicked.connect(lambda: self.btn_clear_predict("ResNet"))

        self.timer_camera.timeout.connect(lambda: self.camera_show(self.camera, self.Ui.label_camera))
        self.timer_yolo_predict.timeout.connect(lambda: self.camera_show(self.yolo_camera, self.Ui.label_yolo_predict))
        # self.draw_batch_signal.connect(self.draw_batch)
        # self.draw_epoch_signal.connect(self.draw_epoch)

    def load_dataset(self,flag):
        """
        加载数据集路径
        :return: filename
        """
        default_path = "D:/PyCharm2020/PyTorch/PlantVillage"
        if flag == "data_dir_ResNet":
            filename=QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件夹", default_path)
            self.Ui.lineEdit.setText(filename)
            return filename
        elif flag == "netpath_ResNet":
            filename, _= QtWidgets.QFileDialog.getOpenFileName(self, "❄⚽选取模型参数文件", default_path,
                                                               "*.pth;;*.pkl")
            self.Ui.lineEdit_predict_netpath.setText(filename)
            return filename
        elif flag == "imgpath_ResNet":
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "🎞选取图片文件",default_path,
                                                                "*.JPG;;*.jpg;;*.PNG;;*.png;;All Files(*)")
            self.Ui.lineEdit_predict_imgpath.setText(filename)
            self.draw_pic(self.Ui.textBrowser, filename)
            return filename
        elif flag == "dataset_file":
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "📝选取本地影像文件", default_path,
                                                                "*.mp4;;*.flv;;*.MPEG;;*.AVI;;*.MOV;;*.WMV;;*.JPG;;*.PNG")
            return filename
        elif flag == "camera_pix_path":
            filename= QtWidgets.QFileDialog.getExistingDirectory(self, "🎞选取保存路径", default_path)
            self.Ui.lineEdit_camera_pix_path.setText(filename)
            print(self.Ui.lineEdit_camera_pix_path.text() + "/XHao_pix_img_{}.jpg")
            return filename
    def rootDir(self):
        """
        获取树形目录\n
        current_path：当前工作目录\n
        parent_path：当前工作的父目录\n
        :return: None
        """
        current_path = os.path.dirname(__file__)
        parent_path = os.path.dirname(current_path)
        name = parent_path.split("/")[-1]
        print(parent_path,name)
        # 获取树形目录文件
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(parent_path)
        self.Ui.treeView.setModel(model)
        self.Ui.treeView.setAnimated(True)
        self.Ui.treeView.setSortingEnabled(True)
        self.Ui.treeView.setAlternatingRowColors(True)
        self.Ui.treeView.setRootIndex(model.index(parent_path))

        for i in [1, 2, 3]:
            self.Ui.treeView.setColumnHidden(i, True)

    def train_thread(self,flag):
        self.thread_train = Thread(lambda :self.train(flag))
        self.thread_stop_signal.connect(lambda :self.thread_train.quit())
        # 捕获输出，到窗口显示
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.thread_train.draw_epoch_signal.connect(self.draw_epoch)
        self.thread_train.draw_batch_signal.connect(self.draw_batch)
        if self.Ui.lineEdit.text() == "":
            QtWidgets.QMessageBox.warning(self, "警告！", "参数设置错误！\n无法开始训练，请重试！", QtWidgets.QMessageBox.Yes)

        else:
            self.thread_train.start()
    def train(self,flag):
        """
        训练模型
        :param flag: 网络模型类型
        :return:
        """
        print("\n网络模型 "+flag+"：开始训练数据集。。。。。\n")
        if flag == "ResNet":
            lr = float(self.Ui.doubleSpinBox_LR.text())
            epoch = int(self.Ui.spinBox_epoch.text())
            batchsize = int(self.Ui.spinBox_batch.text())
            floor = self.Ui.comboBox_floor.currentText()
            num_classes = int(self.Ui.spinBox_numbers.text())
            exercise = int(self.Ui.spinBox_exercise.text())
            dataset_path = self.Ui.lineEdit.text() + "/"
            print("数据集地址：",dataset_path)
            try:
                result = Resnet_Train(batch_signal=self.thread_train.draw_batch_signal,epoch_signal=self.thread_train.draw_epoch_signal,epoch=epoch, batchsize=batchsize, floor=floor, num_classes=num_classes, lr=lr,
                                      dataset_path=dataset_path, exercise=exercise)
            except:
                msg = QtWidgets.QMessageBox()
                font = QtGui.QFont()
                font.setFamily("楷体")
                font.setPointSize(17)
                msg.setFont(font)
                msg.warning(self,"警告！","参数设置错误！\n无法开始训练，请重试！",QtWidgets.QMessageBox.Yes)

                self.stop_train()
                return
        elif flag == "UNet":
            lr = float(self.Ui.doubleSpinBox_LR_3.text())
            epoch = int(self.Ui.spinBox_epoch_3.text())
            batchsize = int(self.Ui.spinBox_batch_3.text())
            floor = int(self.Ui.comboBox_floor_3.currentText())
            num_classes = int(self.Ui.spinBox_numbers_3.text())
            exercise = int(self.Ui.spinBox_exercise_3.text())
            dataset_path = self.Ui.lineEdit_4.text()+ "/"
            try:
                result = Resnet_Train(batch_signal=self.draw_batch_signal,epoch_signal=self.draw_epoch_signal,epoch=epoch, batchsize=batchsize, floor=floor, num_classes=num_classes, lr=lr,
                                      dataset_path=dataset_path, exercise=exercise)
            except:
                QtWidgets.QMessageBox.warning(self, "警告！", "参数设置错误！\n无法开始训练，请重试！", QtWidgets.QMessageBox.Yes)
                self.stop_train()
                return
    def stop_train(self):
        print("\r训练中断。")
        self.thread_stop_signal.emit()

    def predict(self,flag):
        if flag == "ResNet_predict":
            img_path = self.Ui.lineEdit_predict_imgpath.text()
            net_path = self.Ui.lineEdit_predict_netpath.text()
            name_json = r"./classes_names_fruit.json"
            if img_path == "" :
                QtWidgets.QMessageBox.warning(self, "⚠","当前没有输入数据路径，请重试！",QtWidgets.QMessageBox.Yes)
                return None
            elif net_path == "":
                QtWidgets.QMessageBox.warning(self, "⚠", "当前没有输入模型参数文件，请重试！", QtWidgets.QMessageBox.Yes)
                return None
            # 显示待检测的图片
            net = Checknet()
            pre_img = net.predict(img_path,net_path,name_json)
            root_path = r"D:/PyCharm2020/plant_scan/update_windows/predict_img/"
            pre_img = root_path + pre_img + ".PNG"
            print(pre_img)
            self.draw_pic(self.Ui.textBrowser_2,pre_img)    # 显示预测的结果
        else:
            print("XHao")
    def btn_clear_predict(self,flag):
        if flag == "ResNet":
            self.Ui.textBrowser.clear()
            self.Ui.textBrowser_2.clear()
            return
        elif flag == "UNet":
            self.Ui.textBrowser_5.clear()
            self.Ui.textBrowser_6.clear()
            return

    def camera_thread(self,flag):
        if flag == "camera":
            self.camera_way = 0  # 0代表调用本机摄像头
            self.Ui.pushButton_open_file.setEnabled(False)
            if self.timer_camera.isActive() == False:
                flag_open = self.camera.open(self.camera_way)
                if flag_open == False:       #相机读取豁免为空，即没有画面
                    QtWidgets.QMessageBox.warning(self, '⚠Warning', '请检测相机与电脑是否连接正确',
                                                        buttons=QtWidgets.QMessageBox.Ok,
                                                        defaultButton=QtWidgets.QMessageBox.Ok)
                else:
                    self.timer_camera.start(30)
                    self.Ui.pushButton_open_camera.setText(u'关闭相机')
            else:
                self.timer_camera.stop()
                self.camera.release()
                self.Ui.label_camera.clear()
                self.Ui.pushButton_open_file.setEnabled(True)
                self.Ui.pushButton_open_camera.setText(u'打开相机')
        elif flag == "file":
            if self.Ui.pushButton_open_file.text() == u'打开影像':
                self.camera_way = self.load_dataset("dataset_file") # 此时camera_way为数据资源路径
            else:
                pass
            self.Ui.pushButton_open_camera.setEnabled(False)
            if self.timer_camera.isActive() == False:
                flag_open = self.camera.open(self.camera_way)
                if flag_open == False:  # 相机读取豁免为空，即没有画面
                    QtWidgets.QMessageBox.warning(self, '⚠Warning', '请检测当前路径文件格式是否正确或者文件是否损坏',
                                                  buttons=QtWidgets.QMessageBox.Ok,
                                                  defaultButton=QtWidgets.QMessageBox.Ok)
                else:
                    self.timer_camera.start(30)
                    self.Ui.pushButton_open_file.setText(u'关闭影像')
            else:
                self.timer_camera.stop()
                self.camera.release()
                self.Ui.label_camera.clear()
                self.Ui.pushButton_open_camera.setEnabled(True)
                self.Ui.pushButton_open_file.setText(u'打开影像')
        else:
            pass
    def camera_show(self,cap,container):
        flag, image = cap.read()
        show = cv2.resize(image, (640, 500))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        container.setPixmap(QtGui.QPixmap.fromImage(showImage))
    def btn_get_camera_pix(self):
        self.count += 1
        camera_dir_path = self.Ui.lineEdit_camera_pix_path.text()
        if not camera_dir_path or camera_dir_path[1:3] != ":/":
            QtWidgets.QMessageBox.warning(self, "✋⛔警告⛔✋", "请设置保存位置！🏚", QtWidgets.QMessageBox.Yes)
            return None
        screen = QtWidgets.QApplication.primaryScreen()
        pix = screen.grabWindow(self.Ui.label_camera.winId())
        camera_pix_path = camera_dir_path + "/XHao_pix_img_{}.jpg".format(self.count)
        pix = pix.scaled(256,256)
        pix.save(camera_pix_path)
        self.Ui.textBrowser_dataset_show.append(camera_pix_path)
        self.draw_pic(self.Ui.textBrowser_dataset_show, camera_pix_path)
        return None

    def draw_pic(self,show_part,img_path):
        """
        :param show_part: 展示图片的控件
        :param img_path: 图片的地址
        :return:
        """
        # cursor = show_part.textCursor()
        # cursor.movePosition(QtGui.QTextCursor.End)
        # cursor.insertText("<img src='{}'>".format(img_path))
        # show_part.setTextCursor(cursor)
        show_part.append("<img src='{}'>".format(img_path))
        show_part.ensureCursorVisible()

    def draw_batch(self,epoch,x_batchloss,y_batchloss,x_batchacc,y_batchacc):
        """
        画实验中数据集的每个batch对应的loss和accuracy
        :param epoch:
        :param x_batchloss:
        :param y_batchloss:
        :param x_batchacc:
        :param y_batchacc:
        :return:
        """
        print(epoch,x_batchloss,y_batchloss,x_batchacc,y_batchacc)
        self.epoch = epoch
        self.figure_batch.axes1.scatter(x_batchloss, y_batchloss)
        self.figure_batch.axes2.scatter(x_batchacc, y_batchacc)
        if self.Ui.checkBox_ResNet.isChecked() and epoch != self.epoch:
            self.figure_batch.fig.savefig("./epoch_{}_loss_acc".format(self.epoch))
    def draw_epoch(self,x_epochloss,y_epochloss,x_epochacc,y_epochacc):
        """
        画每次实验对应的数据集的loss和accuracy
        :param x_epochloss:
        :param y_epochloss:
        :param x_epochacc:
        :param y_epochacc:
        :return:
        """
        print(x_epochloss,y_epochloss,x_epochacc,y_epochacc)
        self.figure_epoch.axes3.scatter(x_epochloss,y_epochloss)
        self.figure_epoch.axes4.scatter(x_epochacc, y_epochacc)
        if self.Ui.checkBox_ResNet.isChecked() and self.epoch == int(self.Ui.spinBox_epoch.text()):
            self.figure_epoch.fig.savefig("./num_{}_all_loss_acc".format(self.Ui.spinBox_exercise.text()))
    def outputWritten(self, text):
        """
        捕获输出内容输出到指定的位置，这里指的是textEdit控件
        :param text: 捕获的输出内容
        :return:
        """
        cursor = self.Ui.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.Ui.textEdit.setTextCursor(cursor)
        self.Ui.textEdit.ensureCursorVisible()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,
                                               'XHao Net Studio confirm',
                                               "是否要退出XHao Net Studio？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UI_logic()
    window.show()
    sys.exit(app.exec_())