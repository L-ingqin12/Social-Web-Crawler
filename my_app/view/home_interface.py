# coding:utf-8
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon, LineEdit

from trash.untitled1 import Ui_MainWindow
from .gallery_interface import GalleryInterface
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet
from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter)
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from qfluentwidgets import LineEdit, PrimaryPushButton

class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)
        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('Social Web Crawler', self)
        self.banner = QPixmap(':/gallery/images/header1.png')
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)

        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub repo'),
            self.tr(
                'Social web crawler captures and analyzes data from Zhihu and Weibo'),
            REPO_URL
        )
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)
        self.vBoxLayout.addWidget(self.themeButton, 0, Qt.AlignRight)
        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        self.themeButton.setToolTip(self.tr('切换主题'))
        self.themeButton.clicked.connect(self.toggleTheme)

    def toggleTheme(self):
        theme = Theme.LIGHT if isDarkTheme() else Theme.DARK
        cfg.set(cfg.themeMode, theme)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), 200
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # draw background color
        if not isDarkTheme():
            painter.fillPath(path, QColor(206, 216, 228))
        else:
            painter.fillPath(path, QColor(0, 0, 0))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        path.addRect(QRectF(0, h, w, self.height() - h))
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea, Ui_MainWindow):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.dataBase = DataBaseWidget(self)
        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.addWidget(self.dataBase)

        # self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """ load samples """


class DataBaseWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setFixedHeight(336)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("widget")
        self.label = QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(110, 40, 731, 25))
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.setGeometry(QtCore.QRect(110, 90, 741, 155))

        self.label_4 = QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.label_5 = QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.label_6 = QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(34)
        self.gridLayout.setObjectName("gridLayout")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.label_5, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.label_6, 0, 4, 1, 1)

        self.submit = PrimaryPushButton(self)
        self.submit.setObjectName("submit")
        self.gridLayout.addWidget(self.submit, 2, 2, 1, 1)

        self.database_url = LineEdit(self)
        self.database_url.setObjectName("database_url")
        self.gridLayout.addWidget(self.database_url, 1, 0, 1, 1)

        self.database_port = LineEdit(self)
        self.database_port.setObjectName("database_port")
        self.gridLayout.addWidget(self.database_port, 1, 1, 1, 1)

        self.database_username = LineEdit(self)
        self.database_username.setObjectName("database_username")
        self.gridLayout.addWidget(self.database_username, 1, 2, 1, 1)

        self.database_password = LineEdit(self)
        self.database_password.setObjectName("database_password")
        self.gridLayout.addWidget(self.database_password, 1, 3, 1, 1)

        self.database_dbname = LineEdit(self)
        self.database_dbname.setObjectName("database_dbname")
        self.gridLayout.addWidget(self.database_dbname, 1, 4, 1, 1)

        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 1)
        # self.gridLayout.setRowStretch(0, 1)
        # self.gridLayout.setRowStretch(1, 1)
        # self.gridLayout.setRowStretch(2, 3)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_3.setText(_translate("MainWindow", "数据库设置"))
        self.label_4.setText(_translate("MainWindow", "用户名"))
        self.submit.setText(_translate("MainWindow", "确认"))
        self.label.setText(_translate("MainWindow", "数据库url"))
        self.label_2.setText(_translate("MainWindow", "port"))
        self.label_5.setText(_translate("MainWindow", "密码"))
        self.label_6.setText(_translate("MainWindow", "数据库名称"))



