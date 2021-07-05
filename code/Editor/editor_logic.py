#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/6/20 23:15 
# ide： PyCharm

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QPushButton
from torch import nn,device,cuda

sys.path.append("..")
from lib.conv_widgets import XLabel
from lib.editor_widgets import Editor_Ui

device = device('cuda' if cuda.is_available() else 'cpu')

class FlattenLayer(nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()

    def forward(self, x):
        return x.view(x.shape[0], -1)

class Editor_logic(Editor_Ui):
    def __init__(self):
        super(Editor_logic, self).__init__()
        self.labels = {}
        self.conv_nums = 0
        self.inputDialog = QInputDialog()
        self.inputDialog.setStyleSheet("""QInputDialog {font: 14pt "楷体";background-color: rgb(0, 0, 243);""")
        self.add_menuAction()
        self.net_init(device=device)
        self.btn = QPushButton(self)
        self.btn.setText("Generate")
        self.btn.clicked.connect(self.__generate)

    def net_init(self,device):
        self.net = nn.Sequential()
        self.net.to(device=device)

    def contextMenuEvent(self, event):
        """
        重写鼠标右击事件，获取点击坐标
        """
        self.__mousePos = event.pos()
        self.context_menu.exec_(event.globalPos())

    def add_menuAction(self):
        # 添加按钮
        self.context_menu.addAction("添加卷积层", self.add_conv)
        self.context_menu.addAction("添加池化层", self.add_pool)
        self.context_menu.addAction("添加全连接层", self.add_fulllink)
        self.context_menu.addAction("添加降维层", self.add_flattenlayer)
        self.context_menu.addSeparator()
        self.context_menu.addAction("添加激活函数", self.add_activation)
        self.context_menu.addSeparator()
        self.context_menu.addAction("添加输出层", self.add_output)


    def add_input(self):
        print("add_input")

    def add_conv(self):
        self.conv_nums += 1
        new_label = XLabel(self, self.conv_nums)
        self.__label_setting(new_label, "卷积层{}\nConvlution".format(self.conv_nums), self.removeConv)
        new_label.move(int(self.__mousePos.x() - new_label.size().width() / 2),
                       int(self.__mousePos.y() - new_label.size().width() / 2))
        flag,inchannals, outchannals, kernel_size, padding = self.__conv_para_setting()
        new_label.show()
        self.net.add_module("卷积层{} Convlution".format(self.conv_nums),
                                 nn.Conv2d(inchannals, outchannals, kernel_size, padding))
        self.labels[str(self.conv_nums)] = new_label

    def add_pool(self):
        self.conv_nums += 1
        new_label = XLabel(self, self.conv_nums)
        self.__label_setting(new_label,"池化层{}\nMaxPool".format(self.conv_nums),self.removeConv)
        new_label.move(int(self.__mousePos.x() - new_label.size().width() / 2),
                       int(self.__mousePos.y() - new_label.size().width() / 2))
        flag,inchannals, outchannals, kernel_size, padding = self.__conv_para_setting()
        new_label.show()
        self.net.add_module("池化层{} MaxPool".format(self.conv_nums),
                                 nn.Conv2d(inchannals, outchannals, kernel_size, padding))
        self.labels[str(self.conv_nums)] = new_label

    def add_fulllink(self):
        print("fulllink")
        self.conv_nums += 1
        new_label = XLabel(self, self.conv_nums)
        self.__label_setting(new_label, "全连接层{}\nMaxPool".format(self.conv_nums), self.removeConv)
        new_label.move(int(self.__mousePos.x() - new_label.size().width() / 2),
                       int(self.__mousePos.y() - new_label.size().width() / 2))
        inchannals, flag_I = self.inputDialog.getInt(None, "设置属性", "设置输入通道数", 3, 1, 1000, 1)
        outchannals, flag_O = self.inputDialog.getInt(None, "设置属性", "设置输出通道数", 3, 1, 1000, 1)
        new_label.show()
        self.net.add_module("全连接层{} FullLink".format(self.conv_nums),nn.Linear(inchannals, outchannals))
        self.labels[str(self.conv_nums)] = new_label

    def add_flattenlayer(self):
        self.conv_nums += 1
        flattenlayer = FlattenLayer()
        new_label = XLabel(self, self.conv_nums)
        self.__label_setting(new_label, "降维层{}\nFlattenLayers".format(self.conv_nums), self.removeConv)
        new_label.move(int(self.__mousePos.x() - new_label.size().width() / 2),
                       int(self.__mousePos.y() - new_label.size().width() / 2))
        new_label.show()
        self.net.add_module("降维层{} FlattenLayers".format(self.conv_nums),flattenlayer)
        self.labels[str(self.conv_nums)] = new_label

    def add_activation(self):
        self.conv_nums += 1
        activations = ["RELU","Sigmoid","TanH"]
        activation,OK = self.inputDialog.getItem(None,"添加激活函数","激活函数类型：",activations)
        if OK:
            new_label = XLabel(self, self.conv_nums)
            self.__label_setting(new_label, "激活函数{}\nactivation".format(self.conv_nums), self.removeConv)
            new_label.move(int(self.__mousePos.x() - new_label.size().width() / 2),
                           int(self.__mousePos.y() - new_label.size().width() / 2))
            new_label.show()
            if activation == "RELU":
                self.net.add_module("激活函数",nn.ReLU())
            elif activation == "Sigmoid":
                self.net.add_module("激活函数",nn.Sigmoid())
            elif activation == "TanH":
                self.net.add_module("激活函数", nn.Tanh())
            self.labels[str(self.conv_nums)] = new_label

    def add_output(self):
        print("output")

    def __label_setting(self,new_label,text,deleteFunc):
        new_label.delete.connect(deleteFunc)
        new_label.setStyleSheet("background-color: rgba(0,0,0,0.3); color: rgb(255,255,255);")
        new_label.setText(text)
        new_label.setAlignment(Qt.AlignCenter)

    def __conv_para_setting(self):
        inchannals, flag_I = self.inputDialog.getInt(None, "设置属性", "设置输入通道数", 3, 1, 1000, 1)
        outchannals, flag_O = self.inputDialog.getInt(None, "设置属性", "设置输出通道数", 3, 1, 1000, 1)
        kernel_size, flag_K = self.inputDialog.getInt(None, "设置属性", "设置卷积核尺寸", 3, 1, 1000, 1)
        padding, flag_P = self.inputDialog.getInt(None, "设置属性", "设置padding尺寸", 0, 1, 1000, 1)
        print(inchannals, outchannals, kernel_size, padding)
        return flag_I and flag_O and flag_K and flag_P,inchannals,outchannals,kernel_size,padding

    def removeConv(self, index):
        try:
            label = self.labels[str(index)]
            label.deleteLater()
            self.updateConv(index)
        except KeyError:
            QMessageBox.information(self, 'open make_conv', '当前此类网络层数为零\n请添加！！ ！！', QMessageBox.Yes)

    def updateConv(self, index):
        del self.net[index - 1]
        for i in range(index, self.conv_nums):
            self.labels[str(i)] = self.labels[str(i + 1)]
            self.labels[str(i)].index -= 1
            text = self.labels[str(i)].text()
            self.labels[str(i)].setText(text[:3] + str(self.labels[str(i)].index) + text[4:])
        del self.labels[str(self.conv_nums)]
        self.conv_nums -= 1

    def __generate(self):
        print(self.net)
        # return self.net


if __name__ == '__main__':
    import sys, cgitb,time
    from PyQt5.QtWidgets import QApplication
    t1 = time.time()
    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    w = Editor_logic()
    w.resize(800, 600)
    t2 = time.time()
    print(t2-t1)
    w.show()
    print(time.time()-t2)
    sys.exit(app.exec_())
