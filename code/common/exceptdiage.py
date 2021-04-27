'''
Author: PiKaChu-wcg
Github: https://github.com/PiKaChu-wcg/
Date: 2021-04-26 13:35:51
LastEditTime: 2021-04-26 15:21:15
LastEditors: PiKaChu-wcg
FilePath: \ViTorch\code\common\exceptdiage.py
Description: 发生异常的时候弹出消息框
'''

from PyQt5.QtWidgets import QMessageBox

def call_except(parent, string='系统崩溃了', exc=None):
    QMessageBox.information(parent, "发生错误", "{1}:{0}".format(string, exc),
                            QMessageBox.Yes)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QPushButton
    import sys
    app = QApplication(sys.argv)
    win = QWidget()
    b = QPushButton(win)
    b.clicked.connect(lambda: call_except(win))
    win.show()
    sys.exit(app.exec_())
