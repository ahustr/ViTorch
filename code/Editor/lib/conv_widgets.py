#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/6/20 23:17 
# ide： PyCharm
from PyQt5.QtCore import pyqtSignal, Qt, QPoint
from PyQt5.QtWidgets import QLabel, QMenu

Style = """
QMenu {
    color: rgba(0,0,0,1);
    /* 半透明效果 */
    background-color: rgba(255, 255, 255, 0.75);
    border: none;
    border-radius: 4px;
}
QMenu::item {
    border-radius: 5px;
    /* 这个距离很麻烦需要根据菜单的长度和图标等因素微调 */
    padding: 8px 48px 8px 36px; /* 36px是文字距离左侧距离*/
    background-color: transparent;
}
/* 鼠标悬停和按下效果 */
QMenu::item:selected {
    border-radius: 10px;
    /* 半透明效果 */
    background-color: rgba(255,200,200,1);
}
/* 禁用效果 */
QMenu::item:disabled {
    background-color: transparent;
}
/* 图标距离左侧距离 */
QMenu::icon {
    left: 15px;
}
/* 分割线效果 */
QMenu::separator {
    height: 1px;
    background-color: rgb(232, 236, 230);
}
"""


class XLabel(QLabel):
    delete = pyqtSignal(object)
    add = pyqtSignal(object,str)
    link = pyqtSignal(object)
    setParamater = pyqtSignal(object)
    def __init__(self,parent=None,index=None,pre = None,next = None):
        super(XLabel, self).__init__(parent)
        self.index = index
        self.next = next
        self.pre = pre
        self.LPos = self.pos() + QPoint(0, int(self.size().height() / 2))
        self.RPos = self.LPos + QPoint(self.size().width(),0)
        self.resize(120,90)
        self.move_enabled = False
        self.setupUI()

    def setupUI(self):
        self.setScaledContents(True)
        self.context_menu = QMenu(self)
        self.context_menu.setStyleSheet(Style)
        self.init_menu()

    def init_menu(self):
        self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        self.context_menu.setWindowFlags(self.context_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        # 添加按钮
        add_ = QMenu(parent=self.context_menu,title="插入")
        add_.addAction("添加卷积层", self.__add_conv)
        add_.addAction("添加池化层", self.__add_pool)
        add_.addAction("添加激活函数", self.__add_activation)
        add_.addSeparator()
        add_.addAction("添加降维层", self.__add_flattenlayer)
        add_.addAction("添加全连接层", self.__add_Linear)
        add_.addSeparator()
        add_.addAction("添加批量归一化卷积层", self.__add_BatchNorm2d)
        add_.addAction("添加批量归一化全连接层", self.__add_BatchNorm1d)
        add_.addAction("添加丢弃层", self.__add_Dropout)
        self.context_menu.addMenu(add_)
        self.context_menu.addAction("删除",self.__delete)
        self.context_menu.addSeparator()
        self.context_menu.addAction("链接", self.__link)
        self.context_menu.addSeparator()
        # self.context_menu.addAction("参数设置", self.__setParamater)

    def __delete(self):
        self.delete.emit(self.index)

    def __add(self):
        self.add.emit(self.index)

    def __link(self):
        self.link.emit(self.index)

    def __setParamater(self):
        self.setParamater.emit(self.index)

    def __add_conv(self):
        self.add.emit(self.index, "self.add_conv")
    def __add_pool(self):
        self.add.emit(self.index, "self.add_pool")
    def __add_activation(self):
        self.add.emit(self.index, "self.add_activation")
    def __add_flattenlayer(self):
        self.add.emit(self.index, "self.add_flattenlayer")
    def __add_Linear(self):
        self.add.emit(self.index, "self.add_Linear")
    def __add_BatchNorm2d(self):
        self.add.emit(self.index, "self.add_BatchNorm2d")
    def __add_BatchNorm1d(self):
        self.add.emit(self.index, "self.add_BatchNorm1d")
    def __add_Dropout(self):
        self.add.emit(self.index, "self.add_Dropout")

    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())

    def mousePressEvent(self, mouse_event):
        if mouse_event.button() == Qt.LeftButton:
            self.initial_pos = self.pos()
            self.global_pos = mouse_event.globalPos()
            self.move_enabled = True

    def mouseMoveEvent(self, mouse_event):
        parent_height,parent_width = self.parent().size().height(),self.parent().size().width()
        height,width = self.size().height(),self.size().width()
        if self.move_enabled:
            diff = mouse_event.globalPos() - self.global_pos
            current_pos = self.initial_pos + diff
            current_x,current_y = current_pos.x(), current_pos.y()
            if current_x >= 15 - width and current_x <= parent_width  - 15 and current_y >= 15 - height and current_y <= parent_height - 15 :
                self.movePos(current_x,current_y)
            else:
                pass

    def movePos(self,a0:QPoint.x,a1:QPoint.y):
        self.move(a0,a1)
        self.LPos = self.pos() + QPoint(0, self.size().height() / 2)
        self.RPos = self.LPos + QPoint(self.size().width(), 0)
        self.parent().update()

    def mouseReleaseEvent(self, mouse_event):
        if self.move_enabled:
            self.move_enabled = False

if __name__ == '__main__':
    import sys, cgitb,time
    from PyQt5.QtWidgets import QApplication
    t1 = time.time()
    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    w = XLabel()
    w.resize(800, 600)
    t2 = time.time()
    print(t2-t1)
    w.show()
    print(time.time()-t2)
    sys.exit(app.exec_())