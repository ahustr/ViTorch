#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/5/4 15:23 
# ide： PyCharm
import os,sys

from PySide2 import QtGui, QtCore

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import time
import cv2
from PySide2.QtCore import QObject, Slot, Signal, QPropertyAnimation
from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QFileDialog
from PySide2.QtWebChannel import QWebChannel

from ViTorch.code.dataloader.Xlib.datasets_ui import Ui_Form
from ViTorch.code.dataloader.XThread import XThread
from ViTorch.code.dataloader.XprogressDialog import download_rate

class Xpy_js(QObject):
    """
     一个槽函数供js调用(内部最终将js的调用转化为了信号),
     一个信号供js绑定,
     这个一个交互对象最基本的组成部分.
     """
    # 定义信号,该信号会在js中绑定一个js方法.
    sig_send_to_js = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 交互对象接收到js调用后执行的py回调函数.
        self.receive_data_from_js_callback = None

    @Slot(list)
    def receive_data_from_js(self, list):
        print('收到前端data: ', list)
        self.receive_data_from_js_callback(list)

class XDatasets(QWidget):
    def __init__(self,parent=None):
        super(XDatasets, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.pages.setCurrentIndex(0)
        self.channel_init()
        self.slot_init()
        self.ui.label.setMinimumHeight(self.height()-1)
        self.download_thread = []
        self.count = 0

    def slot_init(self):
        self.ui.pushButton_get_current.setEnabled(False)
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.timer_yolo_predict = QtCore.QTimer()
        self.camera = cv2.VideoCapture()
        self.timer_camera.timeout.connect(lambda: self.camera_show(self.camera, self.ui.label_camera))

        self.ui.webEngineView.loadStarted.connect(lambda: self.ui.label.setText("正在加载..."))
        self.ui.webEngineView.loadFinished.connect(lambda: self.init_slide(self.height() - 1, 50))
        self.ui.btn_slide.clicked.connect(self.menu_slide)
        self.ui.btn_online.clicked.connect(lambda :self.ui.pages.setCurrentIndex(0))
        self.ui.btn_diy.clicked.connect(lambda :self.ui.pages.setCurrentIndex(1))
        self.ui.pushButton_open_file.clicked.connect(lambda: self.diy_datasets("file"))
        self.ui.pushButton_open_camera.clicked.connect(lambda: self.diy_datasets("camera"))
        self.ui.pushButton_get_current.clicked.connect(self.btn_get_camera_pix)
        self.ui.btn_load_pix_path.clicked.connect(lambda: self.load_datasets_path("camera_pix_path"))

    def channel_init(self):
        self.Xpyforjs = Xpy_js(self)  # 实例化QWebChannel的前端处理对象
        self.Xpyforjs.receive_data_from_js_callback = self.receive_data_from_js     #py对前端返回的数据处理函数
        self.webchannel = QWebChannel(self.ui.webEngineView.page())
        self.webchannel.registerObject('Xpyforjs', self.Xpyforjs)  # 将前端处理对象在前端页面中注册为名Xpyforjs
        self.ui.webEngineView.page().setWebChannel(self.webchannel)  # 挂载前端处理对象

    def receive_data_from_js(self,url_list):
        reply = QMessageBox.question(self,'数据集 选择/下载','当前选择的数据集为 {}，\n    是否下载使用？'.format(url_list[0]),QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            dirpath = os.getcwd() + '\\XDatasets\\' + url_list[0]
            os.makedirs(dirpath, exist_ok=True)
            for url in url_list[1:]:
                print(url)
                thread = XThread(lambda :self.download_link(thread,dirpath,url))
                thread.str_float.connect(self.dialog_update)
                self.download_thread.append(thread)
                thread.start()
                time.sleep(0.25)

    def download_link(self,thread_name,dirpath,url):
        filename = url.split('/')[-1]
        filepath = dirpath + '/' + filename
        print(filepath)
        download_rate(thread_name,filepath,url)

    def dialog_update(self,info,rate):
        self.ui.label.setText(info)
    
    def init_slide(self,startheight,minimumHeight):
        """
        左边菜单动画
        :return:
        """
        self.ui.label.setText("加载完毕！")
        cur_height = int(startheight)
        end_height = int(minimumHeight)
        self.ui.label.setMinimumHeight(minimumHeight)
        animate = QPropertyAnimation(self.ui.label,b'maximumHeight',self)
        animate.setDuration(800)
        animate.setStartValue(cur_height)
        animate.setEndValue(end_height)
        animate.start()
        animate.finished.connect(lambda :self.ui.label.setText("~请选择相关数据集~"))

    def menu_slide(self):
        """
        左边菜单动画
        :return:
        """
        cur_width = self.ui.left_menu.width()
        if cur_width == 140:
            end_width = 295
            self.ui.btn_slide.setText("收起")
        else:
            end_width = 140
            self.ui.btn_slide.setText("展开")
        animate = QPropertyAnimation(self.ui.left_menu, b'minimumWidth', self)
        animate.setDuration(400)
        animate.setStartValue(cur_width)
        animate.setEndValue(end_width)
        animate.start()

    def diy_datasets(self,flag):
        if flag == "camera":
            self.camera_way = 0  # 0代表调用本机摄像头
            self.ui.pushButton_open_file.setEnabled(False)
            if self.timer_camera.isActive() == False:
                flag_open = self.camera.open(self.camera_way)
                if flag_open == False:       #相机读取画面为空，即没有画面
                    QMessageBox.warning(self, '⚠Warning', '请检测相机与电脑是否连接正确',buttons=QMessageBox.Ok,defaultButton=QMessageBox.Ok)
                else:
                    self.timer_camera.start(30)
                    self.ui.pushButton_open_camera.setText(u'关闭相机')
                    self.ui.pushButton_get_current.setEnabled(True)
            else:
                self.timer_camera.stop()
                self.camera.release()
                self.ui.label_camera.clear()
                self.ui.pushButton_open_file.setEnabled(True)
                self.ui.pushButton_open_camera.setText(u'打开相机')
                self.ui.pushButton_get_current.setEnabled(False)

        elif flag == "file":
            if self.ui.pushButton_open_file.text() == u'打开影像':
                self.camera_way = self.load_datasets_path("datasets_file") # 此时camera_way为数据资源路径
            self.ui.pushButton_open_camera.setEnabled(False)
            if self.timer_camera.isActive() == False:
                flag_open = self.camera.open(self.camera_way)
                if flag_open == False:  # 相机读取豁免为空，即没有画面
                    QMessageBox.warning(self, '⚠Warning', '请检测当前路径文件格式是否正确或者文件是否损坏',buttons=QMessageBox.Ok,defaultButton=QMessageBox.Ok)
                else:
                    self.timer_camera.start(30)
                    self.ui.pushButton_open_file.setText(u'关闭影像')
                    self.ui.pushButton_get_current.setEnabled(True)

            else:
                self.timer_camera.stop()
                self.camera.release()
                self.ui.label_camera.clear()
                self.ui.pushButton_open_camera.setEnabled(True)
                self.ui.pushButton_get_current.setEnabled(False)
                self.ui.pushButton_open_file.setText(u'打开影像')
        else:
            pass

    def camera_show(self, cap, container):
        flag, image = cap.read()
        # image = cv2.flip(image,1)
        show = cv2.resize(image, (640, 500))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        container.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def btn_get_camera_pix(self):
        camera_dir_path = self.ui.lineEdit_camera_pix_path.text()
        if not camera_dir_path or camera_dir_path[1:3] != ":/":
            QMessageBox.warning(self, "✋⛔警告⛔✋", "请设置保存位置！🏚", QMessageBox.Yes)
            return None
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(self.ui.label_camera.winId())
        label = "train" if self.ui.rad_train.isChecked() else "test"# camera_pix_path = camera_dir_path + label +"/XHao_pix_img_{}.jpg".format(self.count)
        os.makedirs(camera_dir_path + '/' + label,exist_ok=True)
        camera_pix_path = camera_dir_path + '/' + label + "/XHao_pix_img_{}.jpg".format(self.count)
        self.count += 1
        pix = pix.scaled(256,256)
        pix.save(camera_pix_path)
        self.ui.textBrowser_dataset_show.append(camera_pix_path)
        self.draw_pic(self.ui.textBrowser_dataset_show, camera_pix_path)
        return None

    def load_datasets_path(self,flag):
        global filename
        default_path = os.getcwd()
        if flag == "datasets_file":
            filename, _ = QFileDialog.getOpenFileName(self, "📝选取本地影像文件", default_path,
                                                                "*.mp4;;*.flv;;*.MPEG;;*.AVI;;*.MOV;;*.WMV;;*.JPG;;*.PNG")
        elif flag == "camera_pix_path":
            filename = QFileDialog.getExistingDirectory(self, "🎞选取保存路径", default_path)
            self.ui.lineEdit_camera_pix_path.setText(filename)
            camera_pix_path = self.ui.lineEdit_camera_pix_path.text() + "/train/" + "XHao_pix_img_{}.jpg".format(self.count)
            print(camera_pix_path)
        return filename

    def draw_pic(self,show_part,img_path):
        """
        :param show_part: 展示图片的控件
        :param img_path: 图片的地址
        :return:
        """
        show_part.append("<img src='{}'>".format(img_path))
        show_part.ensureCursorVisible()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'VIXorch confirm',
                                     "是否要退出 数据集模块 ？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.close()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = XDatasets()
    win.show()
    sys.exit(app.exec_())
