import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread


class VideoProcessor(QThread):

    img_redy_signal = pyqtSignal()
    processor_stopped_signal = pyqtSignal()

    sourceVideo = -1
    current_frames = {}

    def __init__(self):
        super().__init__()
        self._run_flag = False
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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
        # self.exit(0)
        self._run_flag = False
        self.current_frames = {}
        self.processor_stopped_signal.emit()
        # self.wait()
        self.exit(0)
        self.processor_stopped_signal.emit()

    def is_started(self):
        return self._run_flag


    def processor(self, cv_img):
        self.current_frames['original'] = cv_img
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        self.current_frames['gray'] = gray


        cv_result = cv_img.copy()
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face

        for (x, y, w, h) in faces:
            cv2.rectangle(cv_result, (x, y), (x + w, y + h), (255, 0, 0), 2)
        self.current_frames['result'] = cv_result
        self.img_redy_signal.emit()
