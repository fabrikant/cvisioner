import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)


if __name__ == "__main__":
    print(sys.argv)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())