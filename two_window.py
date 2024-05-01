import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow
from PySide6.QtCore import QTimer
from pyqtgraph import PlotWidget, plot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('主窗体')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()
        button = QPushButton('打开子窗口', self)
        button.clicked.connect(self.open_subwindow)
        layout.addWidget(button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_subwindow(self):
        self.subwindow = SubWindow()
        self.subwindow.show()

class SubWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('子窗口')
        self.setGeometry(600, 300, 800, 600)

        self.plot_widget = PlotWidget(self)
        self.plot_widget.setGeometry(10, 10, 780, 580)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

        self.x = list(range(100))
        self.y = [random.randint(0, 10) for _ in range(100)]

    def update_plot(self):
        self.y.pop(0)
        self.y.append(random.randint(0, 10))
        self.plot_widget.clear()
        self.plot_widget.plot(self.x, self.y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
