import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread


class VideoProcessor(QThread):
    img_redy_signal = pyqtSignal()
    sourceVideo = -1
    current_frames = {}

    def __init__(self):
        super().__init__()
        self._run_flag = False

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.sourceVideo)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.current_frames['original'] = cv_img

                gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                self.current_frames['gray'] = gray

                self.img_redy_signal.emit()

        # shut down capture system
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def is_started(self):
        return self._run_flag