# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'datasets_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import QWebEngineView


from VIXorch.Xlib import dataset_resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1192, 794)
        Form.setStyleSheet(u"#Form{background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.94, fx:0.495025, fy:0.488, stop:0.0845771 rgba(151, 225, 229, 255), stop:1 rgba(255, 255, 255, 255));}")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.left_menu = QWidget(Form)
        self.left_menu.setObjectName(u"left_menu")
        self.left_menu.setMinimumSize(QSize(140, 0))
        self.left_menu.setMaximumSize(QSize(295, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.left_menu)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, -1)
        self.toggle = QWidget(self.left_menu)
        self.toggle.setObjectName(u"toggle")
        self.toggle.setMaximumSize(QSize(16777215, 50))
        self.toggle.setStyleSheet(u"#toggle{border-bottom:2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.724, fx:0.5, fy:0.506, stop:0.0845771 rgba(246, 136, 22, 255), stop:1 rgba(255, 255, 255, 255))}")
        self.verticalLayout_4 = QVBoxLayout(self.toggle)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 2)
        self.btn_slide = QPushButton(self.toggle)
        self.btn_slide.setObjectName(u"btn_slide")
        self.btn_slide.setMinimumSize(QSize(140, 40))
        self.btn_slide.setMaximumSize(QSize(150, 16777215))
        font = QFont()
        font.setFamily(u"\u6977\u4f53")
        font.setPointSize(16)
        self.btn_slide.setFont(font)
        self.btn_slide.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(154, 154, 154,0.5);\n"
"	border-radius:10px}\n"
"QPushButton::hover{\n"
"	border:2px solid rgb(0, 0, 0)}\n"
"QPushButton::pressed{\n"
"	color: rgb(255, 0, 0);}")
        icon = QIcon()
        icon.addFile(u":/newPrefix/resources/2.5D\u5b57\u6bcdM.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_slide.setIcon(icon)
        self.btn_slide.setIconSize(QSize(40, 40))

        self.verticalLayout_4.addWidget(self.btn_slide)


        self.verticalLayout_2.addWidget(self.toggle, 0, Qt.AlignHCenter)

        self.btn_fun_select = QWidget(self.left_menu)
        self.btn_fun_select.setObjectName(u"btn_fun_select")
        self.btn_fun_select.setStyleSheet(u"")
        self.btn_online = QPushButton(self.btn_fun_select)
        self.btn_online.setObjectName(u"btn_online")
        self.btn_online.setGeometry(QRect(0, 10, 291, 50))
        self.btn_online.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(22)
        self.btn_online.setFont(font1)
        self.btn_online.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(179, 179, 179, 1);\n"
"	color: rgb(0, 0, 0);\n"
"	border-radius:10px;}\n"
"QPushButton::hover{\n"
"	background-color: rgba(179, 179, 179, 0.5);\n"
"border:2px solid rgb(0, 0, 0);\n"
"	border-radius:10px;}\n"
"QPushButton::pressed{\n"
"background-color: rgba(179, 179, 179, 1);\n"
"border-radius:10px;\n"
"};")
        icon1 = QIcon()
        icon1.addFile(u":/newPrefix/resources/online.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_online.setIcon(icon1)
        self.btn_online.setIconSize(QSize(45, 45))
        self.btn_diy = QPushButton(self.btn_fun_select)
        self.btn_diy.setObjectName(u"btn_diy")
        self.btn_diy.setGeometry(QRect(0, 65, 291, 50))
        self.btn_diy.setMinimumSize(QSize(0, 0))
        self.btn_diy.setFont(font1)
        self.btn_diy.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(179, 179, 179, 1);\n"
"	color: rgb(0, 0, 0);\n"
"	border-radius:10px;}\n"
"QPushButton::hover{\n"
"	background-color: rgba(179, 179, 179, 0.5);\n"
"border:2px solid rgb(0, 0, 0);\n"
"	border-radius:10px;}\n"
"QPushButton::pressed{\n"
"background-color: rgba(179, 179, 179, 1);\n"
"border-radius:10px;\n"
"};")
        icon2 = QIcon()
        icon2.addFile(u":/newPrefix/resources/diy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_diy.setIcon(icon2)
        self.btn_diy.setIconSize(QSize(45, 45))

        self.verticalLayout_2.addWidget(self.btn_fun_select)

        self.widget_2 = QWidget(self.left_menu)
        self.widget_2.setObjectName(u"widget_2")

        self.verticalLayout_2.addWidget(self.widget_2)


        self.horizontalLayout.addWidget(self.left_menu)

        self.pages = QStackedWidget(Form)
        self.pages.setObjectName(u"pages")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.page)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.webEngineView = QWebEngineView(self.splitter)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setMinimumSize(QSize(0, 0))
        font2 = QFont()
        font2.setFamily(u"\u6977\u4f53")
        font2.setPointSize(14)
        self.webEngineView.setFont(font2)
        self.webEngineView.setAutoFillBackground(False)
        self.webEngineView.setStyleSheet(u"border:None;")
        self.webEngineView.setZoomFactor(1.000000000000000)
        self.splitter.addWidget(self.webEngineView)
        self.label = QLabel(self.splitter)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 50))
        self.label.setMaximumSize(QSize(16777215, 100))
        self.label.setFont(font2)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet(u"background:transparent;")
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setOpenExternalLinks(True)
        self.splitter.addWidget(self.label)

        self.verticalLayout.addWidget(self.splitter)

        self.pages.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_3 = QVBoxLayout(self.page_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 20)
        self.diy_camera_widget = QWidget(self.page_2)
        self.diy_camera_widget.setObjectName(u"diy_camera_widget")
        self.horizontalLayout_15 = QHBoxLayout(self.diy_camera_widget)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_camera = QLabel(self.diy_camera_widget)
        self.label_camera.setObjectName(u"label_camera")
        self.label_camera.setFont(font)
        self.label_camera.setStyleSheet(u"background-color: rgba(104, 104, 104, 0.1);")
        self.label_camera.setMidLineWidth(0)
        self.label_camera.setTextFormat(Qt.AutoText)
        self.label_camera.setScaledContents(True)
        self.label_camera.setAlignment(Qt.AlignCenter)
        self.label_camera.setOpenExternalLinks(True)

        self.horizontalLayout_15.addWidget(self.label_camera)

        self.line = QFrame(self.diy_camera_widget)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"background-color: rgb(170, 255, 255);")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_15.addWidget(self.line)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEdit_camera_pix_path = QLineEdit(self.diy_camera_widget)
        self.lineEdit_camera_pix_path.setObjectName(u"lineEdit_camera_pix_path")
        self.lineEdit_camera_pix_path.setMinimumSize(QSize(0, 30))
        font3 = QFont()
        font3.setFamily(u"\u6977\u4f53")
        font3.setPointSize(10)
        self.lineEdit_camera_pix_path.setFont(font3)
        self.lineEdit_camera_pix_path.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.lineEdit_camera_pix_path.setAlignment(Qt.AlignCenter)
        self.lineEdit_camera_pix_path.setClearButtonEnabled(True)

        self.horizontalLayout_6.addWidget(self.lineEdit_camera_pix_path)

        self.btn_load_pix_path = QPushButton(self.diy_camera_widget)
        self.btn_load_pix_path.setObjectName(u"btn_load_pix_path")
        font4 = QFont()
        font4.setFamily(u"\u6977\u4f53")
        font4.setPointSize(12)
        self.btn_load_pix_path.setFont(font4)
        icon3 = QIcon()
        icon3.addFile(u":/newPrefix/resources/file.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_load_pix_path.setIcon(icon3)
        self.btn_load_pix_path.setIconSize(QSize(40, 40))

        self.horizontalLayout_6.addWidget(self.btn_load_pix_path)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, -1, -1, -1)
        self.rad_test = QRadioButton(self.diy_camera_widget)
        self.rad_test.setObjectName(u"rad_test")
        self.rad_test.setFont(font2)
        self.rad_test.setChecked(True)

        self.horizontalLayout_5.addWidget(self.rad_test)

        self.rad_train = QRadioButton(self.diy_camera_widget)
        self.rad_train.setObjectName(u"rad_train")
        self.rad_train.setFont(font2)

        self.horizontalLayout_5.addWidget(self.rad_train)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.textBrowser_dataset_show = QTextBrowser(self.diy_camera_widget)
        self.textBrowser_dataset_show.setObjectName(u"textBrowser_dataset_show")
        self.textBrowser_dataset_show.setFont(font4)
        self.textBrowser_dataset_show.setLayoutDirection(Qt.LeftToRight)
        self.textBrowser_dataset_show.setStyleSheet(u"border:none;\n"
"background-color: rgba(104, 104, 104, 0.1);")
        self.textBrowser_dataset_show.setLineWrapMode(QTextEdit.NoWrap)

        self.verticalLayout_5.addWidget(self.textBrowser_dataset_show)


        self.horizontalLayout_15.addLayout(self.verticalLayout_5)

        self.horizontalLayout_15.setStretch(0, 5)
        self.horizontalLayout_15.setStretch(1, 1)

        self.verticalLayout_3.addWidget(self.diy_camera_widget)

        self.diy_btn_widget = QWidget(self.page_2)
        self.diy_btn_widget.setObjectName(u"diy_btn_widget")
        self.horizontalLayout_4 = QHBoxLayout(self.diy_btn_widget)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(50, 0, 50, 0)
        self.pushButton_open_camera = QPushButton(self.diy_btn_widget)
        self.pushButton_open_camera.setObjectName(u"pushButton_open_camera")
        self.pushButton_open_camera.setMinimumSize(QSize(0, 40))
        self.pushButton_open_camera.setFont(font2)

        self.horizontalLayout_4.addWidget(self.pushButton_open_camera)

        self.pushButton_get_current = QPushButton(self.diy_btn_widget)
        self.pushButton_get_current.setObjectName(u"pushButton_get_current")
        self.pushButton_get_current.setMinimumSize(QSize(0, 40))
        self.pushButton_get_current.setFont(font2)
        self.pushButton_get_current.setStyleSheet(u"color:rgb(255, 0, 0);")

        self.horizontalLayout_4.addWidget(self.pushButton_get_current)

        self.pushButton_open_file = QPushButton(self.diy_btn_widget)
        self.pushButton_open_file.setObjectName(u"pushButton_open_file")
        self.pushButton_open_file.setMinimumSize(QSize(0, 40))
        self.pushButton_open_file.setFont(font2)
        self.pushButton_open_file.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.pushButton_open_file)


        self.verticalLayout_3.addWidget(self.diy_btn_widget)

        self.pages.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.pages)


        self.retranslateUi(Form)

        self.pages.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_slide.setText(QCoreApplication.translate("Form", u"\u5c55\u5f00", None))
        self.btn_online.setText(QCoreApplication.translate("Form", u"    online", None))
        self.btn_diy.setText(QCoreApplication.translate("Form", u"      diy   ", None))
        self.label.setText(QCoreApplication.translate("Form", u"1236", None))
        self.label_camera.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u672a\u68c0\u6d4b\u5230\u6444\u50cf\u5934!\n"
"\n"
"~_~\u8bf7\u6253\u5f00\u6444\u50cf\u5934\u6216\u8005\u52a0\u8f7d\u672c\u5730\u8d44\u6e90~_~", None))
        self.lineEdit_camera_pix_path.setPlaceholderText(QCoreApplication.translate("Form", u"\u56fe\u7247\u4fdd\u5b58\u6587\u4ef6\u5939", None))
        self.btn_load_pix_path.setText("")
        self.rad_test.setText(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u96c6", None))
        self.rad_train.setText(QCoreApplication.translate("Form", u"\u8bad\u7ec3\u96c6", None))
#if QT_CONFIG(statustip)
        self.textBrowser_dataset_show.setStatusTip(QCoreApplication.translate("Form", u"\u5c55\u793a\u83b7\u53d6\u7684\u5e27", None))
#endif // QT_CONFIG(statustip)
        self.textBrowser_dataset_show.setPlaceholderText(QCoreApplication.translate("Form", u"\u83b7\u53d6\u7684\u5e27", None))
        self.pushButton_open_camera.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u76f8\u673a", None))
        self.pushButton_get_current.setText(QCoreApplication.translate("Form", u"\u6355\u83b7\u5f53\u524d\u5e27", None))
        self.pushButton_open_file.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u5f71\u50cf", None))
    # retranslateUi

