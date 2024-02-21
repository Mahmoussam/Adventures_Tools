import win32gui
import win32process
import win32con
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor
from PyQt5 import QtCore
def show_window_by_process_name(process_name):
    hwnd = win32gui.FindWindow(None, process_name)
    if hwnd != 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

def hide_window_by_process_name(process_name):
    hwnd = win32gui.FindWindow(None, process_name)
    print(hwnd)
    if hwnd != 0:
        print('zak',hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

def show_window_by_hwnd(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

def hide_window_by_hwnd(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)





class FullScreenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Full Screen App")
        self.showFullScreen()
        self.activateWindow()
        self.initUI()

    def initUI(self):
        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)
        layout.addStretch()

        # Create the first button and add it to the layout
        button1 = QPushButton("Show", self)
        button1.setStyleSheet("background-color: red; color: white;")
        button1.clicked.connect(self.onButton1Click)
        layout.addWidget(button1, alignment=QtCore.Qt.AlignCenter)

        # Create the second button and add it to the layout
        button2 = QPushButton("Hide", self)
        button2.setStyleSheet("background-color: green; color: white;")
        button2.clicked.connect(self.onButton2Click)
        layout.addWidget(button2, alignment=QtCore.Qt.AlignCenter)

        layout.addStretch()
    hwnd =0x000E01CC
    def onButton1Click(self):
        print("Button show clicked!")
        show_window_by_hwnd(self.hwnd)

    def onButton2Click(self):
        print("Button Hide clicked!")
        hide_window_by_hwnd(self.hwnd)

if __name__ == "__main__":
    #hwnd =0x000709AC #win32gui.FindWindow(None, "timer_.bat - Notepad")
    app = QApplication(sys.argv)
    window = FullScreenApp()
    sys.exit(app.exec_())
    
