#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/5/3 14:27 
# ide： PyCharm
from PyQt5 import QtCore
from PyQt5.QtCore import QMutex, QWaitCondition, QThread

class XThread(QThread):
    """
    自定义线程、支持跨平台X
    """
    time_update = QtCore.pyqtSignal(str)
    valuechanged = QtCore.pyqtSignal(int)
    signal = QtCore.pyqtSignal(str)
    str_float = QtCore.pyqtSignal(str,float)
    def __init__(self,fun):
        super(XThread, self).__init__()
        self.fun = fun
        self.__pause = False
        self.__running = True  # 将running设置为True
        self.__mutex = QMutex()
        self.cond = QWaitCondition()

    def run(self):
        while self.__running:  # 如果被设置为了true就继续，false就终止了
            print("当前线程id：", int(QThread.currentThreadId()))
            self.flag_wait()
            ###################
            self.fun()
            ###################
            self.stopThread()

    def is_runing(self):
        return self.__running

    def flag_wait(self):
        self.__mutex.lock()
        if self.__pause:
            self.cond.wait(self.__mutex)
        self.__mutex.unlock()

    def suspendThread(self):
        self.__pause = True # 设置为True, 让线程阻塞

    def resumeThread(self):
        self.__pause = False    # 设置为False, 让线程停止阻塞
        self.cond.wakeOne()     # 唤醒挂起的线程

    def stopThread(self):
        self.__running = False  # 设置为False
        self.__pause = False
        print("\n停止当前线程{}。".format(int(self.currentThreadId())))
        self.quit()