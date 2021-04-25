import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Combo(QComboBox):
    def __init__(self, title, parent):
        super(Combo, self).__init__(parent)
        #设置为可接受拖曳操作文本
        self.setAcceptDrops(True)
    #当执行一个拖曳控件操作，并且鼠标指针进入该控件时，这个事件将会被触发。
    # 在这个事件中可以获得被操作的窗口控件，还可以有条件地接受或拒绝该拖曳操作

    def dragEnterEvent(self, e):
        #检测拖曳进来的数据是否包含文本，如有则接受，无则忽略
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()
    #当拖曳操作在其目标控件上被释放时，这个事件将被触发

    def dropEvent(self, e):
        #添加拖曳文本到条目中
        self.addItem(e.mimeData().text())


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        #表单布局，添加控件
        lo = QFormLayout()
        lo.addRow(QLabel('请把左边的文本拖曳到右边的下拉菜单中'))
        #实例化单行文本框，设置为允许拖曳操作
        edit = QLineEdit()
        edit.setDragEnabled(True)
        #实例化Combo对象，添加控件到布局中
        com = Combo('Button', self)
        com.setAcceptDrops(True)
        lo.addRow(edit, com)
        #设置主窗口布局及标题
        self.setLayout(lo)
        self.setWindowTitle('简单的拖曳例子')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
