#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/6/26 13:17 
# ide： PyCharm
import os
import sys
import time

import numpy as np
import torch.utils.data
import torchvision
from PyQt5.QtCore import QObject, pyqtSignal
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from torch import cuda,device
from torchvision import transforms, datasets

device = device('cuda' if cuda.is_available() else 'cpu')
pro_path = os.path.abspath("./").replace("\\","/")
class Train(QObject):
    batch_loss = pyqtSignal(int,list,list,list,list)
    batch_acc = pyqtSignal(int,list,list,list,list)
    def __init__(self):
        super(Train, self).__init__()

    # 读取数据
    def load_data_fashion_mnist(self,batch_size, resize=None, root='./Datasets/FashionMNIST'):
        """Download the fashion mnist dataset and then load into memory."""
        trans = []
        if resize:
            trans.append(torchvision.transforms.Resize(size=resize))
        trans.append(torchvision.transforms.ToTensor())

        transform = torchvision.transforms.Compose(trans)
        mnist_train = torchvision.datasets.FashionMNIST(root=root, train=True, download=True, transform=transform)
        mnist_test = torchvision.datasets.FashionMNIST(root=root, train=False, download=True, transform=transform)
        if sys.platform.startswith('win'):
            num_workers = 0  # 0表示不用额外的进程来加速读取数据
        else:
            num_workers = 4
        train_iter = torch.utils.data.DataLoader(mnist_train, batch_size=batch_size, shuffle=True,
                                                 num_workers=num_workers)
        test_iter = torch.utils.data.DataLoader(mnist_test, batch_size=batch_size, shuffle=False,
                                                num_workers=num_workers)
        return train_iter, test_iter

    def evaluate_accuracy(self,data_iter, net, device=None):
        if device is None and isinstance(net, torch.nn.Module):
            # 如果没指定device就使用net的device
            device = list(net.parameters())[0].device
        acc_sum, n = 0.0, 0
        with torch.no_grad():
            for X, y in data_iter:
                if isinstance(net, torch.nn.Module):
                    net.eval()  # 评估模式, 这会关闭dropout
                    acc_sum += (net(X.to(device)).argmax(dim=1) == y.to(device)).float().sum().cpu().item()
                    net.train()  # 改回训练模式
                else:
                    if ('is_training' in net.__code__.co_varnames):  # 如果有is_training这个参数
                        # 将is_training设置成False
                        acc_sum += (net(X, is_training=False).argmax(dim=1) == y).float().sum().item()
                    else:
                        acc_sum += (net(X).argmax(dim=1) == y).float().sum().item()
                n += y.shape[0]
        return acc_sum / n

    # 训练
    def __train(self,net, train_iter, test_iter, optimizer, device, num_epochs,save):
        net = net.to(device)
        print("training on ", device)
        loss = torch.nn.CrossEntropyLoss()
        best_acc = 0.0
        for epoch in range(num_epochs):
            batch_loss = [0 for _ in range(1,len(train_iter)+1)]
            batch_acc = [0 for _ in range(1,len(train_iter)+1)]
            train_l_sum, train_acc_sum, n, batch_count, start = 0.0, 0.0, 0, 0, time.time()
            for step, data in enumerate(train_iter,start=0):
                img, label = data
                img = img.to(device)
                label = label.to(device)
                label_hat = net(img)
                l = loss(label_hat, label)
                optimizer.zero_grad()
                l.backward()
                optimizer.step()
                train_l_sum += l.cpu().item()
                train_acc_sum += (label_hat.argmax(dim=1) == label).sum().cpu().item()
                n += label.shape[0]
                batch_loss[step] = l.item()
                batch_count += 1
                x_batchloss = np.arange(1, len(train_iter) + 1, 1)
                y_batchloss = batch_loss
                x_batchacc = np.arange(1, len(train_iter) + 1, 1)
                y_batchacc = batch_acc
                self.batch_loss.emit(epoch,x_batchloss.tolist(),y_batchloss,x_batchacc.tolist(),y_batchacc)
                rate = (step + 1) / len(train_iter)
                a = "*" * int(rate * 50)
                b = "." * int((1 - rate) * 50)
                print("\r train loss: {:^3.0f}%[{}->{}]{:.4f}".format(int(rate * 100), a, b, l),end="")
            test_acc = self.evaluate_accuracy(test_iter, net)
            if save:
                if test_acc > best_acc:
                    best_acc = test_acc
                    torch.save(net.state_dict(), pro_path + "/ViTorch_moudle.pth")
            print('epoch %d, loss %.4f, train acc %.3f, test acc %.3f, time %.1f sec'
                  % (epoch, train_l_sum / batch_count, train_acc_sum / n, test_acc, time.time() - start))

    def train(self,net, train_iter, test_iter,optimizer, device, num_epochs,save):
        # train_iter, test_iter = self.load_data_fashion_mnist(batch_size, resize=224)
        self.__train(net, train_iter, test_iter, optimizer, device, num_epochs,save=save)

    def load_datasets(self,rootpath,batchsize,resize=256):
        # 图像预处理
        data_transform = {
            "train": transforms.Compose([transforms.RandomResizedCrop(224),  # 对图片尺寸做一个缩放切割
                                         transforms.RandomHorizontalFlip(),  # 水平翻转
                                         transforms.ToTensor(),  # 转化为张量
                                         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),

            "val": transforms.Compose([transforms.Resize(resize),
                                       transforms.CenterCrop(224),
                                       transforms.ToTensor(),
                                       transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])}
        try:
            train_dataset = datasets.ImageFolder(root= rootpath + "train", transform=data_transform["train"])
            train_iter = torch.utils.data.DataLoader(train_dataset, batch_size=batchsize, shuffle=True,num_workers=0)

            validate_dataset = datasets.ImageFolder(root=rootpath + "val", transform=data_transform["val"])
            validate_iter = torch.utils.data.DataLoader(validate_dataset,batch_size=batchsize, shuffle=False, num_workers=0)
            All_dataset = datasets.ImageFolder(root=rootpath)
            return train_iter,validate_iter,All_dataset
        except FileNotFoundError:
            return None,None,None

class Matplotlib_qt_figure(FigureCanvas):
    """
    定义一个画图的接口，用于pyqt5和matplotlib的链接，即在pyqt上面显示matplotlib图像
    """
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(Matplotlib_qt_figure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        FigureCanvas.updateGeometry(self)