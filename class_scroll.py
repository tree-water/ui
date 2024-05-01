from time import perf_counter
import numpy as np
import pyqtgraph as pg
# from PySide6.QtWidgets import QDialog

class ScrollingPlots():
    def __init__(self):
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('pyqtgraph example: Scrolling Plots')
        self.chunkSize = 100
        self.maxChunks = 10
        self.startTime = perf_counter()
        self.p5 = self.win.addPlot(colspan=2)
        self.p5.setLabel('bottom', 'Time', 's')
        self.p5.setXRange(-10, 0)
        self.curves = []
        self.data = np.empty((self.chunkSize+1,2))
        self.ptr5 = 0

    def update1(self):
        now = perf_counter()
        for c in self.curves:
            c.setPos(-(now-self.startTime), 0)

        i = self.ptr5 % self.chunkSize
        if i == 0:
            curve = self.p5.plot()
            self.curves.append(curve)
            last = self.data[-1]
            self.data = np.empty((self.chunkSize+1,2))        
            self.data[0] = last
            while len(self.curves) > self.maxChunks:
                c = self.curves.pop(0)
                self.p5.removeItem(c)
        else:
            curve = self.curves[-1]
        self.data[i+1,0] = now - self.startTime
        self.data[i+1,1] = np.random.normal()
        curve.setData(x=self.data[:i+2, 0], y=self.data[:i+2, 1])
        self.ptr5 += 1
        self.p5.setYRange(-3, 3)


    def scroll(self):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update1)
        timer.start(50)
        pg.exec()

scroll = ScrollingPlots()
scroll.scroll()