import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap
from VideoProcessor import *
from VideoFrame import *


class MainWindow(QMainWindow):

    stop_processing = False

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)
        self.videoProcessor = VideoProcessor()
        self.videoProcessor.img_redy_signal.connect(self.next_frame_finished)
        self.videoProcessor.processor_stopped_signal.connect(self.on_processor_stopped)
        app.aboutToQuit.connect(self.stop_video_processor)
        self.mdiArea = self.findChild(QMdiArea, 'mdiArea')
        self.frameList = self.findChild(QListWidget, 'frameList')


    def next_frame_finished(self):
        if self.stop_processing:
            return
        sub_windows = self.mdiArea.subWindowList()
        for id_frame, cv_img in self.videoProcessor.current_frames.items():
            need_to_show = True
            sub_window_is_find = False
            find_items = self.frameList.findItems(id_frame, Qt.MatchExactly)
            if len(find_items) == 0:
                list_item = QListWidgetItem(id_frame)
                list_item.setCheckState(Qt.CheckState.Checked)
                self.frameList.addItem(list_item)
            else:
                if find_items[0].checkState() != 2:
                    need_to_show = False

            for sub_window in sub_windows:
                if sub_window.id_frame == id_frame:
                    sub_window_is_find = True
                    # print('isHide', sub_window.isHidden(), 'isVisible', sub_window.isVisible())
                    if need_to_show:
                        sub_window.current_frame = cv_img.copy()
                        sub_window.update_image()
                        if sub_window.isHidden():
                            sub_window.show()
                    else:
                        self.mdiArea.removeSubWindow(sub_window)
                    break
            if need_to_show and not sub_window_is_find:
                sub_window = VideoFrame(id_frame)
                self.mdiArea.addSubWindow(sub_window)
                sub_window.current_frame = cv_img.copy()
                sub_window.show()

    def start_video_processor(self, video_source):
        self.stop_processing = False
        if self.videoProcessor.is_started():
            self.videoProcessor.stop()
        self.videoProcessor.sourceVideo = video_source
        self.videoProcessor._run_flag = True
        self.videoProcessor.start()


    def on_processor_stopped(self):
        self.frameList.clear()
        self.mdiArea.closeAllSubWindows()


    def stop_video_processor(self):
        self.stop_processing = True
        self.videoProcessor.stop()

    def start_capture(self):
        self.start_video_processor(-1)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, caption='Open file')[0]
        if filename != '':
            self.start_video_processor(filename)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
