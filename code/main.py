#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/6/26 19:49
# ide： PyCharm

if __name__ == '__main__':
    from mainWindow.mainwindow_logic import *
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QIcon
    import cgitb, sys

    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    window = mainWindowFunction()
    window.show()
    sys.exit(app.exec_())
