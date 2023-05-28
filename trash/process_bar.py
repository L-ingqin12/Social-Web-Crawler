from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from utils.weibo import get_all_comment_weibo


class DataThread(QThread):
    data_ready = pyqtSignal()

    def run(self):
        # 在这里进行数据准备的操作
        # ...

        # 数据准备完成后发出信号
        self.data_ready.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建按钮并连接槽函数
        self.button = QPushButton('Start', self)
        self.button.clicked.connect(self.start_data_thread)

    def start_data_thread(self):
        # 创建数据准备线程
        self.data_thread = DataThread()
        self.data_thread.data_ready.connect(self.show_main_window)

        # 创建进度条弹窗
        self.progress_dialog = QProgressDialog('Loading...', 'Cancel', 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.resize(300,400)
        self.progress_dialog.show()
        get_all_comment_weibo("4905352364036293")
        # 启动数据准备线程
        self.data_thread.start()

    def show_main_window(self):
        # 关闭进度条弹窗
        self.progress_dialog.close()

        # 打开主界面
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
