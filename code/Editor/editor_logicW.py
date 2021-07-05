#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/6/20 23:15 
# ide： PyCharm
import os
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from torch import nn, device, cuda

from Editor.lib.conv_widgets import XLabel
from Editor.lib.editor_widgets import Editor_Ui

device = device('cuda' if cuda.is_available() else 'cpu')
pro_path = os.path.abspath("./")
class FlattenLayer(nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()

    def forward(self, x):
        return x.view(x.shape[0], -1)

class Editor_logic(Editor_Ui):
    def __init__(self):
        super(Editor_logic, self).__init__()
        self.conv_nums = 0
        self.inputDialog = QInputDialog()
        self.inputDialog.setStyleSheet("""QInputDialog {font: 14pt "楷体";background-color: rgb(0, 0, 243);}""")
        self.labels = {}
        self.lines = []
        self.__mousePos = self.pos() + QPoint(50,50)
        self.__stopPaint = False
        self.currentIndex = 0
        self.__add_newNet_floor = False
        self.add_menuAction()
        self.net_init(device=device)

    def net_init(self,device):
        self.net = nn.Sequential()
        self.net.to(device=device)

    def contextMenuEvent(self, event):
        """
        重写鼠标右击事件，获取点击坐标
        """
        self.__mousePos = event.pos()
        self.context_menu.exec_(event.globalPos())

    def paintEvent(self, event):
        if not self.__stopPaint:
            painter = QPainter(self)
            self.drawLines(painter,self.currentIndex)

    def drawLines(self,painter,currentIndex):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidLine))
        if self.currentIndex == 0 or len(self.labels) == 1:
            pass
        else:
            # # 重头开始连线
            # for i in range(1, len(self.labels)):
            # 当前层往后连线
            for i in range(1 if self.__add_newNet_floor else currentIndex, len(self.labels)):
                line = [self.labels[str(i)].RPos, self.labels[str(i+1)].LPos]
                painter.drawLine(line[0].x(), line[0].y(), line[1].x(), line[1].y())
        self.__add_newNet_floor = True

    def __drawLine(self, index):
        self.__add_newNet_floor = False
        self.currentIndex = index
        self.__stopPaint = False
        self.update()

    def add_menuAction(self):
        # 添加按钮
        self.context_menu.addAction("添加卷积层", self.add_conv)
        self.context_menu.addAction("添加池化层", self.add_pool)
        self.context_menu.addAction("添加激活函数", self.add_activation)
        self.context_menu.addSeparator()
        self.context_menu.addAction("添加降维层", self.add_flattenlayer)
        self.context_menu.addAction("添加全连接层", self.add_Linear)
        self.context_menu.addSeparator()
        self.context_menu.addAction("添加批量归一化卷积层", self.add_BatchNorm2d)
        self.context_menu.addAction("添加批量归一化全连接层", self.add_BatchNorm1d)
        self.context_menu.addAction("添加丢弃层", self.add_Dropout)

    def add_conv(self):
        inputed,inchannals, outchannals, kernel_size, stride, padding = self.__conv_para_setting()
        if inputed:
            new_label = XLabel(self, self.currentIndex+1)
            self.__label_setting(new_label, "{}\n卷积层\nConvlution".format(self.currentIndex+1), self.removeConv,self.__drawLine,self.addChildFunc)
            self.net.add_module("{} Conv".format(self.conv_nums),nn.Conv2d(inchannals, outchannals, kernel_size, stride, padding))
            self.addChildUpdateConv(new_label)
            new_label.show()

    def add_pool(self):
        kernel_size, flag_I = self.inputDialog.getInt(None, "设置属性", "设置形状", 3, 1, 1000, 1)
        stride, flag_II = self.inputDialog.getInt(None, "设置属性", "设置步幅", 2, 1, 1000, 1)
        padding, flag_O = self.inputDialog.getInt(None, "设置属性", "设置填充", 0, 0, 1000, 1)
        if flag_O and flag_I and flag_II:
            new_label = XLabel(self, self.currentIndex+1)
            self.__label_setting(new_label,"{}\n最大池化层\nMaxPool2d".format(self.currentIndex+1),self.removeConv,self.__drawLine,self.addChildFunc)
            self.net.add_module("{} MaxPool".format(self.conv_nums),nn.MaxPool2d( kernel_size, stride, padding))
            self.addChildUpdateConv(new_label)
            new_label.show()

    def add_Linear(self):
        num_inputs, flag_I = self.inputDialog.getInt(None, "设置属性", "设置输入数目", 3, 1, 2**20, 1)
        num_outputs, flag_O = self.inputDialog.getInt(None, "设置属性", "设置输出数目", 3, 1, 2**20, 1)
        if flag_O and flag_I :
            new_label = XLabel(self, self.currentIndex+1)
            self.__label_setting(new_label, "{}\n全连接层\nLinear".format(self.currentIndex+1), self.removeConv,self.__drawLine,self.addChildFunc)
            self.net.add_module("{} Linear".format(self.conv_nums),nn.Linear(num_inputs, num_outputs))
            self.addChildUpdateConv(new_label)
            new_label.show()

    def add_flattenlayer(self):
        flattenlayer = FlattenLayer()
        new_label = XLabel(self, self.currentIndex+1)
        self.__label_setting(new_label, "{}\n降维层\nFlattenLayers".format(self.currentIndex+1), self.removeConv,self.__drawLine,self.addChildFunc)
        self.net.add_module("{} FlattenLayers".format(self.conv_nums),flattenlayer)
        self.addChildUpdateConv(new_label)
        new_label.show()

    def add_Dropout(self):
        drop_prob, flag_I = self.inputDialog.getDouble(None, "设置属性", "设置丢弃概率" , 0, 0, 5.0, 2)
        if flag_I:
            new_label = XLabel(self, self.currentIndex+1)
            self.__label_setting(new_label, "{}\n丢弃层\nDropout".format(self.currentIndex+1), self.removeConv,self.__drawLine,self.addChildFunc)
            self.net.add_module("{} Dropout".format(self.conv_nums),nn.Dropout(drop_prob))
            self.addChildUpdateConv(new_label)
            new_label.show()

    def add_BatchNorm1d(self):
        out_channels, flag_O = self.inputDialog.getInt(None, "设置属性", "设置输出通道数目", 3, 1, 2**20, 1)
        if flag_O:
            new_label = XLabel(self, self.currentIndex+1)
            self.__label_setting(new_label, "{}\n批量归一化\n全连接\nBatchNormal1d".format(self.currentIndex+1), self.removeConv,self.__drawLine,self.addChildFunc)
            self.net.add_module("{} BatchNormal".format(self.conv_nums),nn.BatchNorm1d(out_channels))
            self.addChildUpdateConv(new_label)
            new_label.show()

    def add_BatchNorm2d(self):
        out_channels, flag_O = self.inputDialog.getInt(None, "设置属性", "设置输出通道数目", 3, 1, 2**20, 1)
        if flag_O:
            new_label = XLabel(self, self.currentIndex+1)
            self.__label_setting(new_label, "{}\n批量归一化\n卷积\nBatchNormal2d".format(self.currentIndex+1), self.removeConv,self.__drawLine,self.addChildFunc)
            self.net.add_module("{} BatchNormal".format(self.conv_nums),nn.BatchNorm2d(out_channels))
            self.addChildUpdateConv(new_label)
            new_label.show()

    def add_activation(self):
        activations = ["ReLU","Sigmoid","Tanh"]
        activation,OK = self.inputDialog.getItem(None,"添加激活函数","激活函数类型：",activations)
        if OK:
            new_label = XLabel(self, self.currentIndex + 1)
            self.__label_setting(new_label, "{}\n激活函数\n{}".format(new_label.index,activation), self.removeConv,self.__drawLine,self.addChildFunc)
            if activation == "ReLU":
                self.net.add_module("{} {}".format(self.conv_nums,activation),nn.ReLU())
            elif activation == "Sigmoid":
                self.net.add_module("{} {}".format(self.conv_nums,activation),nn.Sigmoid())
            elif activation == "Tanh":
                self.net.add_module("{} {}".format(self.conv_nums,activation), nn.Tanh())
            self.addChildUpdateConv(new_label)
            new_label.show()

    def __label_setting(self,new_label,text,removeFunc,linkFunc,addChildFunc=None,setParamaterFunc=None):
        self.__add_newNet_floor = True
        self.currentIndex = new_label.index
        new_label.delete.connect(removeFunc)
        new_label.link.connect(linkFunc)
        new_label.add.connect(addChildFunc)
        new_label.setStyleSheet("font: 10pt '黑体';background-color: rgba(0,0,0,0.3); color: rgb(255,255,255);")
        new_label.setText(text)
        new_label.setAlignment(Qt.AlignCenter)
        new_label.movePos(int(self.__mousePos.x() - new_label.size().width() / 2),int(self.__mousePos.y() - new_label.size().width() / 2))

    def addChildFunc(self, currentIndex, Child):
        self.currentIndex = currentIndex
        eval(Child)()

    def addChildUpdateConv(self,new_label):
        self.conv_nums += 1
        newindex = new_label.index
        # 新成员插入字典当中的"newindex"位置
        # # 移位
        newNet = self.net[self.conv_nums - 1]
        for i in range(self.conv_nums, newindex, -1):
            self.labels[str(i)] = self.labels[str(i-1)]
            self.labels[str(i)].index += 1
            self.labels[str(i)].setText(str(self.labels[str(i)].index) + self.labels[str(i)].text()[1:])
            self.net[i-1] = self.net[i-2]
        #  # 插入
        self.labels[str(newindex)] = new_label
        self.net[newindex-1] = newNet

    def __conv_para_setting(self):
        inchannals, flag_I = self.inputDialog.getInt(None, "设置属性", "设置输入通道数", 1, 1, 2**20, 1)
        outchannals, flag_O = self.inputDialog.getInt(None, "设置属性", "设置输出通道数", 1, 1, 2**20, 1)
        kernel_size, flag_K = self.inputDialog.getInt(None, "设置属性", "设置卷积核尺寸", 1, 1, 1000, 1)
        stride, flag_K = self.inputDialog.getInt(None, "设置属性", "设置步长", 1, 1, 1000, 1)
        padding, flag_P = self.inputDialog.getInt(None, "设置属性", "设置padding尺寸", 0, 0, 1000, 1)
        return flag_I and flag_O and flag_K and flag_P, inchannals, outchannals, kernel_size, stride, padding

    def removeConv(self, currentindex):
        try:
            label = self.labels[str(currentindex)]
            label.deleteLater()
            self.removedupdateConv(currentindex)
            self.update()
        except KeyError:
            QMessageBox.information(self, 'open make_conv', '当前此类网络层数为零\n请添加！！ ！！', QMessageBox.Yes)

    def removedupdateConv(self, currentindex):
        print(currentindex,self.conv_nums)
        for i in range(currentindex, self.conv_nums):
            self.labels[str(i)] = self.labels[str(i + 1)]
            self.net[i-1] = self.net[i]
            self.labels[str(i)].index -= 1
            text = self.labels[str(i)].text()
            self.labels[str(i)].setText(str(self.labels[str(i)].index) + text[1:])
        try:
            del self.net[self.conv_nums-1]
            del self.labels[str(self.conv_nums)]
        except:
            print("Failed!")
        self.conv_nums -= 1
        self.currentIndex = self.conv_nums

    def __generate(self):
        dirpath = pro_path + '\\generated'
        os.makedirs(dirpath, exist_ok=True)
        with open(dirpath + '\\ViTorchNet.py',"w") as f:
            f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: XHao
from torch import nn
from torch import Tensor

class ViTorchNet(nn.Module):
    def __init__(self):
        super(ViTorchNet, self).__init__()
        self.layers = nn.Sequential(\n""")
            for data in self.net:
                if str(data) ==  "FlattenLayer()":
                    f.write('\t\t\t' +str(data)+ ',\n')
                else:
                    f.write('\t\t\tnn.' +str(data)+ ',\n')
            f.write("""\t\t)
    def forward(self,x: Tensor) -> Tensor:
        return self.layers(x)
        
class FlattenLayer(nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()

    def forward(self, x):
        return x.view(x.shape[0], -1)""")
        QMessageBox.information(None,"Information","\tVitorch generate successfully!\t\n\n\t{}".format(dirpath + '\\ViTorchNet.py'),QMessageBox.Yes)

    def generate(self):
        self.__generate()

if __name__ == '__main__':
    import sys, cgitb
    from PyQt5.QtWidgets import QApplication
    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    w = Editor_logic()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec_())

# Done!
# training on  cuda
# epoch 1, loss 10.0532, train acc 0.613, test acc 0.757, time 148.7 sec
# epoch 2, loss 0.5522, train acc 0.794, test acc 0.793, time 144.2 sec
# epoch 3, loss 0.4634, train acc 0.828, test acc 0.841, time 150.1 sec
# epoch 4, loss 0.4073, train acc 0.850, test acc 0.842, time 151.1 sec
# epoch 5, loss 0.3620, train acc 0.867, test acc 0.862, time 161.5 sec