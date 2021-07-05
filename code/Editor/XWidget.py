#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/5/3 16:09 
# ide： PyCharm

from math import floor, pi, cos, sin
from random import random, randint
from time import time

from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QWidget, QApplication

__Author__ = 'XHao'
__Copyright__ = 'Copyright (c) 2019'

# 最小和最大半径、半径阈值和填充圆的百分比
from PyQt5.QtWidgets import QMenu, QMessageBox, QLabel,QInputDialog

radMin = 10
radMax = 80
filledCircle = 30  # 填充圆的百分比
concentricCircle = 60  # 同心圆百分比
radThreshold = 25  # IFF special, over this radius concentric, otherwise filled
# 最小和最大移动速度
speedMin = 0.3
speedMax = 0.6
# 每个圆和模糊效果的最大透明度
maxOpacity = 0.6

colors = [
    QColor(52, 168, 83),
    QColor(117, 95, 147),
    QColor(199, 108, 23),
    QColor(194, 62, 55),
    QColor(0, 172, 212),
    QColor(120, 120, 120)
]
circleBorder = 10
backgroundLine = colors[0]
backgroundColor = QColor(38, 43, 46)
backgroundMlt = 0.85

lineBorder = 2.5

# 最重要的是：包含它们的整个圆和数组的数目
maxCircles = 8
points = []

# 实验变量
circleExp = 1
circleExp_Max = 1.003
circleExp_Min = 0.997
circleExpSp = 0.00004
circlePulse = False

# 生成随机整数 a<=x<=b


def randint(a, b):
    return floor(random() * (b - a + 1) + a)

# 生成随机小数


def randRange(a, b):
    return random() * (b - a) + a

# 生成接近a的随机小数


def hyperRange(a, b):
    return random() * random() * random() * (b - a) + a


class Circle:

    def __init__(self, background, width, height):
        self.background = background
        self.x = randRange(-width / 2, width / 2)
        self.y = randRange(-height / 2, height / 2)
        self.radius = hyperRange(radMin, radMax)
        self.filled = (False if randint(
            0, 100) > concentricCircle else 'full') if self.radius < radThreshold else (
                False if randint(0, 100) > concentricCircle else 'concentric')
        self.color = colors[randint(0, len(colors) - 1)]
        self.borderColor = colors[randint(0, len(colors) - 1)]
        self.opacity = 0.05
        self.speed = randRange(speedMin, speedMax)  # * (radMin / self.radius)
        self.speedAngle = random() * 2 * pi
        self.speedx = cos(self.speedAngle) * self.speed
        self.speedy = sin(self.speedAngle) * self.speed
        spacex = abs((self.x - (-1 if self.speedx < 0 else 1) *
                      (width / 2 + self.radius)) / self.speedx)
        spacey = abs((self.y - (-1 if self.speedy < 0 else 1) *
                      (height / 2 + self.radius)) / self.speedy)
        self.ttl = min(spacex, spacey)

Style = """
QMenu {
    color: rgba(0,0,0,1);
    /* 半透明效果 */
    background-color: rgba(255, 255, 255, 0.75);
    border: none;
    border-radius: 4px;
}
QMenu::item {
    border-radius: 4px;
    /* 这个距离很麻烦需要根据菜单的长度和图标等因素微调 */
    padding: 8px 48px 8px 36px; /* 36px是文字距离左侧距离*/
    background-color: transparent;
}
/* 鼠标悬停和按下效果 */
QMenu::item:selected {
    border-radius: 0px;
    /* 半透明效果 */
    background-color: rgba(232, 232, 232, 250);
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
    background-color: rgb(232, 236, 243);
}
"""

class XLabel(QLabel):
    delete = pyqtSignal(object)
    add = pyqtSignal(object)

    def __init__(self,parent=None,index=None):
        super(XLabel, self).__init__(parent)
        self.index = index
        self.resize(100,100)
        self.move_enabled = False
        self.context_menu = QMenu(self)
        self.context_menu.setStyleSheet(Style)
        self.init_menu()

    def init_menu(self):
        self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        self.context_menu.setWindowFlags(self.context_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        # 添加按钮
        self.context_menu.addAction("删除",self.__delete)
        self.context_menu.addAction("添加", self.__add)
        self.context_menu.addSeparator()
        self.context_menu.addAction("链接", self.__add)
        self.context_menu.addSeparator()
        self.context_menu.addAction("参数设置", self.__add)

    def __delete(self):
        self.delete.emit(self.index)

    def __add(self):
        self.add.emit(self.index)

    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())

    def mousePressEvent(self, mouse_event):
        if mouse_event.button() == Qt.LeftButton:
            self.initial_pos = self.pos()
            self.global_pos = mouse_event.globalPos()
            self.move_enabled = True

    def mouseMoveEvent(self, mouse_event):
        global current_pos
        parent_height,parent_width = self.parent().size().height(),self.parent().size().height()
        height,width = self.size().height(),self.size().width()

        if self.move_enabled:
            diff = mouse_event.globalPos() - self.global_pos
            current_pos = self.initial_pos + diff
            current_X = current_pos.x()
            current_y = current_pos.y()
            if current_X > 15 - width and current_X < parent_width  - 15 and current_y > 15 - height and current_y < parent_height - 15 :
                self.move(current_pos)
            else:
                pass

    def mouseReleaseEvent(self, mouse_event):
        if self.move_enabled:
            self.move_enabled = False

class CircleLineWidget(QWidget):
    def __init__(self,parent = None, *args, **kwargs):
        super(CircleLineWidget, self).__init__(parent,*args, **kwargs)
        # 设置背景颜色
        palette = self.palette()
        palette.setColor(palette.Background, backgroundColor)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        # 获取屏幕大小
        geometry = QApplication.instance().desktop().availableGeometry()
        self.screenWidth = geometry.width()
        self.screenHeight = geometry.height()
        self._canDraw = True
        self._firstDraw = True
        self._timer = QTimer(self, timeout=self.update)
        self.labels = {}
        self.conv_nums = 0
        self.context_menu = QMenu(self)
        self.inputDialog = QInputDialog()
        self.init_menu()
        self.init()

    def contextMenuEvent(self, event):
        self.__mousePos = event.pos()
        self.context_menu.exec_(event.globalPos())

    def init_menu(self):
        # 背景透明
        self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        self.context_menu.setWindowFlags(self.context_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        # 添加按钮
        self.context_menu.addAction("添加输入层", self.add_conv_)
        self.context_menu.addSeparator()
        self.context_menu.addAction("添加卷积层",self.add_conv)
        self.context_menu.addSeparator()
        self.context_menu.addAction("添加池化层",self.add_conv_)
        self.context_menu.addSeparator()
        self.context_menu.addAction("添加输出层",self.add_conv_)

    def add_conv(self):
        self.conv_nums += 1
        new_label = XLabel(self,self.conv_nums)
        new_label.delete.connect(self.withdrawnet)
        new_label.setStyleSheet("background-color: rgba(0,0,0,0.3); color: rgb(0,255,0);")
        new_label.setText("卷积层{}\nConvlution".format(self.conv_nums))
        new_label.setAlignment(Qt.AlignCenter)
        new_label.move(int(self.__mousePos.x() - new_label.size().width() / 2 ),
                       int(self.__mousePos.y() - new_label.size().width() / 2 ))
        new_label.show()
        self.labels[str(self.conv_nums)] = new_label

    def add_conv_(self):
        self.conv_nums += 1
        new_label = XLabel(self,self.conv_nums)
        new_label.delete.connect(self.withdrawnet)
        new_label.setStyleSheet("background-color: rgba(0,0,0,0.3); color: rgb(255,255,0);")
        new_label.setText("池化层{}\nConvlution".format(self.conv_nums))
        new_label.setAlignment(Qt.AlignCenter)
        new_label.move(int(self.__mousePos.x() - new_label.size().width() / 2),
                       int(self.__mousePos.y() - new_label.size().width() / 2))
        kernel_size, flag_K = self.inputDialog.getInt(None, "设置属性", "设置卷积核尺寸", 3, 1, 1000, 2)
        inchannals, flag_I = self.inputDialog.getInt(None, "设置属性", "设置输入通道数", 3, 1, 1000, 2)
        outchannals, flag_O = self.inputDialog.getInt(None, "设置属性", "设置输出通道数", 3, 1, 1000, 2)
        padding, flag_P = self.inputDialog.getInt(None, "设置属性", "设置padding尺寸", 0, 1, 1000, 2)
        print(inchannals, outchannals, kernel_size, padding)
        new_label.show()
        self.labels[str(self.conv_nums)] = new_label


    def withdrawnet(self,index):
        try:
            label = self.labels[str(index)]
            label.deleteLater()
            self.updateConv(index)
        except KeyError:
            QMessageBox.information(self, 'open make_conv', '当前此类网络层数为零\n请添加！！ ！！', QMessageBox.Yes)

    def updateConv(self,index):
        for i in range(index, self.conv_nums):
            self.labels[str(i)] = self.labels[str(i + 1)]
            self.labels[str(i)].index -= 1
            text = self.labels[str(i)].text()
            self.labels[str(i)].setText(text[:3] + str(self.labels[str(i)].index) + text[4:])
        del self.labels[str(self.conv_nums)]
        self.conv_nums -= 1

    def init(self):
        points.clear()
        # 链接的最小距离
        self.linkDist = min(self.screenWidth, self.screenHeight) / 2.4
        # 初始化点
        for _ in range(maxCircles * 3):
            points.append(Circle('', self.screenWidth, self.screenHeight))
        self.update()

    def showEvent(self, event):
        super(CircleLineWidget, self).showEvent(event)
        self._canDraw = True

    def hideEvent(self, event):
        super(CircleLineWidget, self).hideEvent(event)
        # 窗口最小化要停止绘制, 减少cpu占用
        self._canDraw = False

    def paintEvent(self, event):
        super(CircleLineWidget, self).paintEvent(event)
        if not self._canDraw:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.draw(painter)

    def draw(self, painter):
        global circleExp,circleExpSp
        if circlePulse:
            if circleExp < circleExp_Min or circleExp > circleExp_Max:
                circleExpSp *= -1
            circleExp += circleExpSp

        painter.translate(self.screenWidth / 2, self.screenHeight / 2)

        if self._firstDraw:
            t = time()
        self.renderPoints(painter, points)
        if self._firstDraw:
            self._firstDraw = False
            # 此处有个比例关系用于设置timer的时间，如果初始窗口很小，没有比例会导致动画很快
            t = (time() - t) * 1000 * 2
            # 比例最大不能超过1920/800
            t = int(min(2.4, self.screenHeight / self.height()) * t) - 1
            t = t if t > 15 else 15  # 不能小于15s
            print('start timer(%d msec)' % t)
            # 开启定时器
            self._timer.start(t)

    def drawCircle(self, painter, circle):
        #         circle.radius *= circleExp
        if circle.background:
            circle.radius *= circleExp
        else:
            circle.radius /= circleExp
        radius = circle.radius

        r = radius * circleExp
        # 边框颜色设置透明度
        c = QColor(circle.borderColor)
        c.setAlphaF(circle.opacity)

        painter.save()
        if circle.filled == 'full':
            # 设置背景刷
            painter.setBrush(c)
            painter.setPen(Qt.NoPen)
        else:
            # 设置画笔
            painter.setPen(
                QPen(c, max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax))))

        # 画实心圆或者圆圈
        painter.drawEllipse(int(circle.x - r), int(circle.y - r), int(2 * r), int(2 * r))
        painter.restore()

        if circle.filled == 'concentric':
            r = radius / 2
            # 画圆圈
            painter.save()
            painter.setBrush(Qt.NoBrush)
            painter.setPen(
                QPen(c, max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax))))
            painter.drawEllipse(int(circle.x - r), int(circle.y - r), int(2 * r), int(2 * r))
            painter.restore()

        circle.x += circle.speedx
        circle.y += circle.speedy
        if (circle.opacity < maxOpacity):
            circle.opacity += 0.01
        circle.ttl -= 1

    def renderPoints(self, painter, circles):
        for i, circle in enumerate(circles):
            if circle.ttl < -20:
                # 重新初始化一个
                circle = Circle('', self.screenWidth, self.screenHeight)
                circles[i] = circle
            self.drawCircle(painter, circle)

        circles_len = len(circles)
        for i in range(circles_len - 1):
            for j in range(i + 1, circles_len):
                deltax = circles[i].x - circles[j].x
                deltay = circles[i].y - circles[j].y
                dist = pow(pow(deltax, 2) + pow(deltay, 2), 0.5)
                # if the circles are overlapping, no laser connecting them
                if dist <= circles[i].radius + circles[j].radius:
                    continue
                # otherwise we connect them only if the dist is < linkDist
                if dist < self.linkDist:
                    xi = (1 if circles[i].x < circles[j].x else -
                          1) * abs(circles[i].radius * deltax / dist)
                    yi = (1 if circles[i].y < circles[j].y else -
                          1) * abs(circles[i].radius * deltay / dist)
                    xj = (-1 if circles[i].x < circles[j].x else 1) * \
                        abs(circles[j].radius * deltax / dist)
                    yj = (-1 if circles[i].y < circles[j].y else 1) * \
                        abs(circles[j].radius * deltay / dist)
                    path = QPainterPath()
                    path.moveTo(circles[i].x + xi, circles[i].y + yi)
                    path.lineTo(circles[j].x + xj, circles[j].y + yj)
#                     samecolor = circles[i].color == circles[j].color
                    c = QColor(circles[i].borderColor)
                    c.setAlphaF(min(circles[i].opacity, circles[j].opacity)
                                * ((self.linkDist - dist) / self.linkDist))
                    painter.setPen(QPen(c, (
                        lineBorder * backgroundMlt if circles[i].background else lineBorder) * (
                        (self.linkDist - dist) / self.linkDist)))
                    painter.drawPath(path)

if __name__ == '__main__':
    import sys, cgitb
    t1 = time()
    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    w = CircleLineWidget()
    w.resize(800, 600)
    t2 = time()
    print(t2 - t1)
    w.show()
    print(time()-t2)
    sys.exit(app.exec_())