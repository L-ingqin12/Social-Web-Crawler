from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QShortcut


class Example(QWidget):
    def __init__(self):
        super().__init__()

        # self.setWindowTitle('Auto Collapse Example')
        self.resize(50, 50)
        self.setWindowFlags(QtCore.Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags()
        # self.setMask(QtGui.QPixmap('dog.png').mask())

        btn = QPushButton('关不掉我吧，哈哈哈！')
        btn.clicked.connect(self.collapse)

        shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        shortcut.activated.connect(self.close)

        vbox = QVBoxLayout()
        vbox.addWidget(btn)

        self.setLayout(vbox)

        self.timer = QTimer()
        self.timer.timeout.connect(self.show)

    def collapse(self):
        self.hide()
        self.timer.start(7000)

    def close(self) -> bool:
        exit(0)
    # 实现拖动，用到了鼠标事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False


if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    ex.show()
    app.exec_()
