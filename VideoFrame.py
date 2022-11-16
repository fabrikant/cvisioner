import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap
from VideoProcessor import *
from PyQt5.QtCore import pyqtSlot, Qt

class VideoFrame(QMdiSubWindow):
    def __init__(self):
        super(VideoFrame, self).__init__()
        uic.loadUi('ui/VideoFrame.ui', self)
        self.videoFrame = self.findChild(QLabel, 'frame')


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.videoFrame.setPixmap(qt_img)


    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.videoFrame.width(), self.videoFrame.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


