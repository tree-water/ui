from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from Ui_UI_show import Ui_Form
import serial
import serial.tools.list_ports as seriallp
import serial.tools.list_ports
import matplotlib.pyplot as plt
from port import Hreader
import keyboard
import time
import threading
import matplotlib.animation as animation
from datetime import datetime
import pyautogui
from serial.serialutil import SerialException, PortNotOpenError

import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow
from PySide6.QtCore import QTimer
from pyqtgraph import PlotWidget, plot

com_x = 'com3'


# ser = serial.Serial()
OK = b'\x00\x00'
Moduletech = b'\x4D\x6F\x64\x75\x6C\x65\x74\x65\x63\x68'

#创建类的实例化
hreader = Hreader(com_x,'01')

def StartToRead():
    hreader.run() # 一键开始盘存


class Mywindow(QWidget, Ui_Form, threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        super().__init__() # 调用父类的构造函数，确保父类中的一些初始化操作得以执行
        self.setupUi(self)

        self.pushButton_stop.clicked.connect(self.StopReadData)
        self.pushButton_start.clicked.connect(self.ReadData)
        self.pushButton_phase.clicked.connect(self.PhaseChart)
        self.pushButton_rssi.clicked.connect(self.RSSIChart)
        self.pushButton_show.clicked.connect(self.DisplayLable)
        self.pushButton_hiderssi.clicked.connect(self.ConcealRSSIChart)
        self.pushButton_hidephase.clicked.connect(self.ConcealPhaseChart)


    def ReadData(self):
        print("开始接收数据。")
        t = threading.Thread(target = StartToRead)
        t.daemon = True  # 将线程 t 设置为守护线程
        t.start() 

    def StopReadData(self):
        print("停止读取数据！")
        pyautogui.hotkey('esc')


    def DisplayLable(self):
        print("展示标签数据")


    def RSSIChart(self):
        print("信号强度图")
        self.RSSI_graph = RSSI()
        self.RSSI_graph.show()


    def ConcealRSSIChart(self):
        print("隐藏信号强度图")


    def PhaseChart(self):
        print("相位图")
        self.Phase_graph = Phase()
        self.Phase_graph.show()


    def ConcealPhaseChart(self):
        print("隐藏相位图")


class RSSI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RSSI')
        self.setGeometry(600, 300, 800, 600)

        self.plot_widget = PlotWidget(self)
        self.plot_widget.setGeometry(10, 10, 780, 580)
        self.plot_widget.setYRange(-90, -10)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

        self.x = list(range(100))
        self.y = [-40 for _ in range(100)]

    def update_plot(self):
        self.y.pop(0)
        self.y.append(hreader.data['RSSI'])
        self.plot_widget.clear()
        self.plot_widget.plot(self.x, self.y)


class Phase(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Phase')
        self.setGeometry(600, 300, 800, 600)

        self.plot_widget = PlotWidget(self)
        self.plot_widget.setGeometry(10, 10, 780, 580)
        self.plot_widget.setYRange(0, 180)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

        self.x = list(range(100))
        self.y = [0 for _ in range(100)]

    def update_plot(self):
        self.y.pop(0)
        self.y.append(hreader.data['phase'])
        self.plot_widget.clear()
        self.plot_widget.plot(self.x, self.y)


if __name__ == '__main__':
    
    # # 新版串口驱动340需添加以下代码
    # try:
    #     p = seriallp.comports()
    #     for pi in p:
    #         # print(pi.device)
    #         _ = pi.device
    #     ser = serial.Serial('COM6')
    #     hreader.port_open('COM6')
    #     # Bootloader()
    #     hreader.port_close()
    # except:
    #     pass

    app = QApplication([])
    window = Mywindow()
    window.show()
    app.exec()
    ui = Mywindow()
    ui.start()

    # 开始读取，数据存在字典dict中，要实时更新显示到图表里（散点）
    # 一个线程读取数据（保活，不杀死），一个线程更新rssi信号强度图，一个线程更新相位phase图，一个线程更新标签列表
    # 预计4个线程，（后面三个线程考虑三合一）
