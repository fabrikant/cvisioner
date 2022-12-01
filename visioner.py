import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap
from VideoProcessor import *
from VideoFrame import *


class MainWindow(QMainWindow):

    stop_processing = False
    media_source = None

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)
        self.videoProcessor = VideoProcessor()
        self.videoProcessor.img_redy_signal.connect(self.next_frame_finished)
        app.aboutToQuit.connect(self.stop_video_processor)
        self.mdiArea = self.findChild(QMdiArea, 'mdiArea')
        self.frameList = self.findChild(QListWidget, 'frameList')
        self.show_status()


    def next_frame_finished(self):
        if self.stop_processing:
            return
        sub_windows = self.mdiArea.subWindowList()
        for id_frame, cv_img in self.videoProcessor.current_frames.items():
            find_items = self.frameList.findItems(id_frame, Qt.MatchExactly)
            if len(find_items) == 0:
                list_item = QListWidgetItem(id_frame)
                list_item.setCheckState(Qt.CheckState.Checked)
                self.frameList.addItem(list_item)
                find_items = self.frameList.findItems(id_frame, Qt.MatchExactly)
            for list_item in find_items:
                if list_item.checkState() == 2:
                    sub_window_find = False
                    for sub_window in sub_windows:
                        if sub_window.id_frame == id_frame:
                            sub_window_find = True
                            sub_window.current_frame = cv_img.copy()
                            sub_window.update_image()
                            if sub_window.isHidden():
                                sub_window.show()
                    if not sub_window_find:
                        sub_window = VideoFrame(id_frame)
                        sub_window.subwindow_close_sigal.connect(self.on_subwindow_close)
                        self.mdiArea.addSubWindow(sub_window)
                        sub_window.show()
                        sub_window.current_frame = cv_img.copy()
                        sub_window.update_image()


    def on_frame_list_changed(self, list_item):
        id_frame = list_item.text()
        sub_windows = self.mdiArea.subWindowList()
        for sub_window in sub_windows:
            if id_frame == sub_window.id_frame:
                if list_item.checkState() == 0 and not sub_window.isHidden():
                    sub_window.close()
                elif list_item.checkState() == 2 and sub_window.isHidden():
                    sub_window.show()

    def on_subwindow_close(self, id_frame):
        find_items = self.frameList.findItems(id_frame, Qt.MatchExactly)
        for list_item in find_items:
            list_item.setCheckState(0)

    def stop_video_processor(self):
        self.stop_processing = True
        self.videoProcessor._run_flag = False
        self.videoProcessor.stop()

    def start_video_processor(self):
        if self.media_source is None:
            return
        self.stop_processing = False
        if self.videoProcessor.is_started():
            self.videoProcessor.stop()
        self.videoProcessor.media_source = self.media_source
        self.videoProcessor._run_flag = True
        self.videoProcessor.start()
        self.show_status()

    def start_capture(self):
        self.media_source = -1
        self.start_video_processor()

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, caption='Open file')[0]
        if filename != '':
            self.media_source = filename
            self.start_video_processor()

    def show_status(self):
        status_bar = self.findChild(QStatusBar, 'statusbar')
        status_string = 'source: '
        if self.media_source == -1:
            status_string += 'web camera'
        else:
            status_string += str(self.media_source)
        status_bar.showMessage(status_string, 0)

    def clear_form(self):
        self.stop_video_processor()
        self.frameList.clear()
        self.mdiArea.closeAllSubWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
