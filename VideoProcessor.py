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
                self.processor(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def is_started(self):
        return self._run_flag

    def add_frame(self, id_frame, cv_img):

        new_key = id_frame
        iter = 0
        # while new_key in self.current_frames:
        #     iter += 1
        #     new_key = str(new_key)+str(iter)
        self.current_frames[new_key] = cv_img

    def processor(self, cv_img):
        self.add_frame('original', cv_img)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        self.add_frame('gray', gray)
        self.add_frame('original1', gray)
        self.img_redy_signal.emit()
