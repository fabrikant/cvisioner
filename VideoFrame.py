import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QPixmap
from VideoProcessor import *
from PyQt5.QtCore import pyqtSlot, Qt


class VideoFrame(QMdiSubWindow):
    id_frame = None
    current_frame = None
    subwindow_close_sigal = pyqtSignal(str)

    def __init__(self, id_frame):
        super(VideoFrame, self).__init__()
        self.id_frame = id_frame
        uic.loadUi('ui/VideoFrame.ui', self)
        self.videoFrame = self.findChild(QLabel, 'frame')
        self.manage_form()

    def manage_form(self):
        geom = self.geometry()
        title_height = self.style().pixelMetric(QStyle.PM_TitleBarHeight)
        self.videoFrame.setGeometry(2, title_height + 2, geom.width() - 4, geom.height() - title_height - 4)
        self.setWindowTitle(str(self.id_frame))
        self.update_image()

    def resizeEvent(self, event):
        self.manage_form()
        return super(VideoFrame, self).resizeEvent(event)

    def closeEvent(self, event):
        self.subwindow_close_sigal.emit(self.id_frame)
        return super(VideoFrame, self).closeEvent(event)

    def update_image(self):
        if not type(self.current_frame) == type(None) and self.isVisible():
            qt_img = self.convert_cv_qt(self.current_frame)
            self.videoFrame.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.videoFrame.width(), self.videoFrame.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
