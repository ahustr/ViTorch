#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/6/20 23:19 
# ide： PyCharm
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMenu, QDialog
from Editor.XWidget import CircleLineWidget
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
    background-color: rgba(230, 230, 230, 0.85);
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
    background-color: rgba(0, 0, 0, 0.75);
}
"""

class Editor_Ui(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(Editor_Ui, self).__init__(parent, *args, **kwargs)
        # 设置背景颜色
        self.setAutoFillBackground(True)
        # 获取屏幕大小
        # self.setStyleSheet("background-color: rgba(255,200,200,1);")
        self.labels = {}
        self.context_menu = QMenu()
        self.context_menu.setStyleSheet(Style)
        self.init_menu()

    def contextMenuEvent(self, event):
        self.__mousePos = event.pos()
        self.context_menu.exec_(event.globalPos())

    def init_menu(self):
        # 背景透明
        self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        self.context_menu.setWindowFlags(self.context_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
