import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedWidget,QLabel,QLineEdit,QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar  # Thêm import này
from NewUI import Ui_MainWindow

class Page1(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label1 = QLabel("Ngôn ngữ nguồn:")
        self.source_language = QLineEdit()

        self.label2 = QLabel("Ngôn ngữ đích:")
        self.target_language = QLineEdit()

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.source_language)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.target_language)

        self.setLayout(self.layout)
class Page2(QWidget):
    def __init__(self):
        super().__init__()

        self.data = []
        self.x_values = []
        self.max_x = 10  # Số lượng điểm trên đồ thị
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGraph)
        self.timer.start(1000)  # Cập nhật dữ liệu mỗi giây

    def initUI(self):
        layout = QVBoxLayout()

        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)

        self.ax.set_xlim(0, self.max_x)
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Realtime Line Graph")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)

    def updateGraph(self):
        if len(self.data) >= self.max_x:
            self.data.pop(0)
            self.x_values.pop(0)
        self.data.append(random.randint(0, 100))
        if not self.x_values:
            self.x_values = list(range(len(self.data)))
        else:
            self.x_values.append(self.x_values[-1] + 1)
        self.line.set_data(self.x_values, self.data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

class Page3(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.connect_button = QPushButton("Kết nối với cổng COM")
        self.layout.addWidget(self.connect_button)

        self.label_widgets = []

        for i in range(8):
            label = QLabel(f"Giá trị Label {i+1}:")
            self.label_widgets.append(label)
            self.layout.addWidget(label)

        self.setLayout(self.layout)
class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.main_win.setWindowFlag(Qt.FramelessWindowHint)
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout(self.uic.StackPage)
        layout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget()
        page1 = Page1()
        page2 = Page2()
        page3 = Page3()
        self.stackedWidget.addWidget(page1)
        self.stackedWidget.addWidget(page2)
        self.stackedWidget.addWidget(page3)

        layout.addWidget(self.stackedWidget)

        self.uic.backBtn.clicked.connect(self.showPreviousBack)
        self.uic.forwardBtn.clicked.connect(self.showNextPage)

    def showPreviousBack(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex()-1)
        
    def showNextPage(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex()+1)
        
    def show(self):
        # command to run
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

