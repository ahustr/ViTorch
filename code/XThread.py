#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/5/3 14:27 
# ide： PyCharm
import ctypes

import win32con
from PyQt5 import QtCore
from PyQt5.QtCore import QMutex, QWaitCondition, QThread
from win32process import ResumeThread, SuspendThread


class XThread(QThread):
    """
    自定义线程、支持跨平台X
    """
    time_update = QtCore.pyqtSignal(str)
    valuechanged = QtCore.pyqtSignal(int)
    signal = QtCore.pyqtSignal(str)
    str_float = QtCore.pyqtSignal(str,float)
    finished = QtCore.pyqtSignal()
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
            self.finished.emit()
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


class XThread_win(QThread):
    """
    自定义线程、仅支持windows系统
    """
    handle_ = -1
    time_update = QtCore.pyqtSignal(str)
    valuechanged = QtCore.pyqtSignal(int)
    signal = QtCore.pyqtSignal(str)
    str_float = QtCore.pyqtSignal(str, float)
    finished = QtCore.pyqtSignal()
    def __init__(self,func):
        super(XThread_win, self).__init__()
        self.func = func

    def run(self):
        try:
            self.handle_ = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
                win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
        except Exception as e:
            print('\nget thread handle failed', e)
        # print('\nthread id', int(QThread.currentThreadId()))
        self.func()
        self.finished.emit()

    def suspendThread(self):
        if self.handle_ == -1:
            print('\nhandle is wrong')
            return False
        ret = SuspendThread(self.handle_)
        # print('\n挂起线程，句柄为', self.handle_, '状态(0:挂起 1:运行)：', ret,'id',int(QThread.currentThreadId()))

    def resumeThread(self):
        if self.handle_ == -1:
            print('\nhandle is wrong')
            return False
        ret = ResumeThread(self.handle_)
        # print('\n恢复线程，句柄为', self.handle_, '状态(0:挂起 1:运行)：', ret,'id',int(QThread.currentThreadId()))

    def stopThread(self):
        ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
            self.handle_, 0)
        # print('\n终止线程,句柄为', self.handle_, ret,'id',int(QThread.currentThreadId()))
        print('\n')
    def is_runing(self):
        return self.is_runing()
