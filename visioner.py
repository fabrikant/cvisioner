import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap
from VideoProcessor import *
from VideoFrame import *

class MainWindow(QMainWindow):
    sub_window = None
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)
        self.videoProcessor = VideoProcessor()
        # self.videoProcessor.img_redy_signal.connect(self.update_image)
        self.mdiArea = self.findChild(QMdiArea, 'mdiArea')
        # self.videoFrame = self.findChild(QLabel, 'videoFrame')

    def start_video_processor(self, video_source):
        if self.videoProcessor.is_started():
            self.videoProcessor.stop()
        self.videoProcessor.sourceVideo = video_source
        self.videoProcessor._run_flag = True
        self.videoProcessor.start()
        if self.sub_window == None:
            self.sub_window = VideoFrame()
            self.videoProcessor.img_redy_signal.connect(self.sub_window.update_image)
            self.mdiArea.addSubWindow(self.sub_window)
            self.sub_window.show()


    def start_capture(self):
        self.start_video_processor(-1)

    def stop_video_processor(self):
        self.videoProcessor.stop()

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, caption='choose file')[0]
        if filename != '':
            self.start_video_processor(filename)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
