import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)

        self.buttonStartCapture = self.findChild(QPushButton, 'buttonStartCapture')
        self.buttonStartCapture.clicked.connect(self.on_mouse_click)

    def on_mouse_click(self):
        print('mouse click')


if __name__ == "__main__":
    print(sys.argv)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
