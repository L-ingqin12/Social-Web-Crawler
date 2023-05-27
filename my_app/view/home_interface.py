# coding:utf-8
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QSpacerItem, QSizePolicy

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon, LineEdit, InfoBar, InfoBarPosition, DropDownPushButton

from trash.untitled1 import Ui_MainWindow

from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet
from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter)
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from qfluentwidgets import LineEdit, PrimaryPushButton

from ..utils.mongoDB_operator import MongoDB

mongodb = None


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

        self.vBoxLayout.addWidget(self.galleryLabel, 0, Qt.AlignLeft)

        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)
        self.vBoxLayout.addWidget(self.themeButton, 0, Qt.AlignRight)
        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        self.themeButton.setToolTip(self.tr('切换主题'))
        self.themeButton.clicked.connect(self.toggleTheme)

        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub repo'),
            self.tr(
                'Social web crawler captures and analyzes data from Zhihu and Weibo'),
            REPO_URL
        )

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
        # self.Ui_DataBase = Ui_DataBase(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        # self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        # self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.addWidget(self.banner)

        # self.vBoxLayout.addWidget(self.Ui_DataBase)

        # self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """ load samples """

        # 将虚线和QSpacerItem添加到每个布局的顶部和底部
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.dataBase = DataBaseWidget(self)
        self.vBoxLayout.addWidget(self.dataBase)

        self.vBoxLayout.addWidget(line)
        self.zhihu_user = ZhiHuUser(self)
        self.vBoxLayout.addWidget(self.zhihu_user)

        self.vBoxLayout.addSpacing(30)
        self.zhihu_other = ZhihuOther(self)
        self.vBoxLayout.addWidget(self.zhihu_other)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        self.vBoxLayout.addWidget(line2)
        self.weibo = WeiBo(self)
        self.vBoxLayout.addWidget(self.weibo)
        self.vBoxLayout.addSpacing(100)


class DataBaseWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(200)
        self.setupUi()
        # StyleSheet.HOME_INTERFACE.apply(self)
        # self.setTheme()

    def setupUi(self):
        self.setGeometry(QtCore.QRect(110, 170, 721, 141))
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

        self.label_2 = QLabel(self.tr("port"), self)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel(self.tr("name"), self)
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
        self.gridLayout.setVerticalSpacing(35)
        self.gridLayout.setObjectName("gridLayout")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 5)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.label_5, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.label_6, 1, 4, 1, 1)

        self.database_url = LineEdit(self)
        self.database_url.setObjectName("database_url")
        self.database_url.setPlaceholderText("localhost")
        self.database_url.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.database_url, 2, 0, 1, 1)

        self.database_port = LineEdit(self)
        self.database_port.setObjectName("database_port")
        self.database_port.setPlaceholderText("27017")
        self.database_port.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.database_port, 2, 1, 1, 1)

        self.database_username = LineEdit(self)
        self.database_username.setObjectName("database_username")
        self.database_username.setPlaceholderText("admin|None")
        self.database_username.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.database_username, 2, 2, 1, 1)

        self.database_password = LineEdit(self)
        self.database_password.setObjectName("database_password")
        self.database_password.setPlaceholderText("admin|None")
        self.database_password.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.database_password, 2, 3, 1, 1)

        self.database_dbname = LineEdit(self)
        self.database_dbname.setObjectName("database_dbname")
        self.database_dbname.setPlaceholderText("mydb")
        self.database_dbname.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.database_dbname, 2, 4, 1, 1)

        self.submit = PrimaryPushButton(self)
        self.submit.setObjectName("submit")
        self.gridLayout.addWidget(self.submit, 3, 2, 1, 1)

        self.submit.clicked.connect(self.connect_database)

        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 1)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 3)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_3.setText(_translate("MainWindow", "数据库设置"))
        self.label_4.setText(_translate("MainWindow", "用户名"))
        self.submit.setText(_translate("MainWindow", "确认"))
        self.label.setText(_translate("MainWindow", "数据库url"))
        self.label_2.setText(_translate("MainWindow", "port"))
        self.label_5.setText(_translate("MainWindow", "密码"))
        self.label_6.setText(_translate("MainWindow", "数据库名称"))

    # def setTheme(self):
    #     StyleSheet.HOME_INTERFACE.apply(self)
    def connect_database(self):
        global mongodb
        database_url = self.database_url.text()
        port = int(self.database_port.text())
        username = self.database_username.text()
        password = self.database_password.text()
        db_name = self.database_dbname.text()
        try:
            if username != "" and password != "":
                mongodb = MongoDB(host=database_url, port=port, db_name=db_name, username=username, password=password)
                # print("登录成功")
            else:
                mongodb = MongoDB(host=database_url, port=port, db_name=db_name)

                # print("登录成功")
            InfoBar.success(
                title="success",
                content="数据库连接成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            print(mongodb)
        except Exception as e:
            InfoBar.error(
                title="error",
                content="e",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,  # won't disappear automatically
                parent=self
            )
            # print("Traceback (most recent call last):", e)
            return None

        return mongodb


class ZhiHuUser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(200)
        self.setupUi()
        # self.setTheme()
        # StyleSheet.HOME_INTERFACE.apply(self)

    def setupUi(self):
        self.zhihu_user = QtWidgets.QVBoxLayout(self)
        self.zhihu_user.setContentsMargins(0, 0, 0, 0)
        self.zhihu_user.setObjectName("zhihu_user")
        self.info = QtWidgets.QHBoxLayout()
        self.info.setObjectName("info")
        self.buttonGroup = QtWidgets.QFormLayout()
        self.buttonGroup.setObjectName("buttonGroup")

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.user_id = LineEdit(self)
        self.user_id.setText("")
        self.user_id.setObjectName("user_id")

        self.get_uer_following = PrimaryPushButton(self)
        self.get_uer_following.setObjectName("get_uer_following")

        self.get_user_follower = PrimaryPushButton(self)
        self.get_user_follower.setObjectName("get_user_follower")

        self.get_user_answers = PrimaryPushButton(self)
        self.get_user_answers.setObjectName("get_user_answers")

        self.get_user_activities = PrimaryPushButton(self)
        self.get_user_activities.setObjectName("get_user_activities")

        self.get_user_info = PrimaryPushButton(self)
        self.get_user_info.setObjectName("get_user_info")

        self.buttonGroup.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.get_uer_following)
        self.buttonGroup.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.get_user_follower)
        self.buttonGroup.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.get_user_answers)
        self.buttonGroup.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.get_user_activities)
        self.buttonGroup.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.get_user_info)

        self.zhihu_user.addWidget(self.label)
        self.info.addWidget(self.user_id)
        self.info.addLayout(self.buttonGroup)

        self.info.setStretch(0, 1)
        self.info.setStretch(1, 1)
        self.zhihu_user.addLayout(self.info)
        self.zhihu_user.setStretch(0, 2)
        self.zhihu_user.setStretch(1, 1)

        self.get_user_activity = DropDownPushButton(self)
        self.get_user_activity.setGeometry(QtCore.QRect(540, 490, 243, 32))
        self.get_user_activity.setObjectName("get_user_activity")
        self.get_user_about = DropDownPushButton(self)
        self.get_user_about.setGeometry(QtCore.QRect(400, 490, 101, 33))
        self.get_user_about.setObjectName("get_user_about")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.label.setText(_translate("get_user_info_by_uid", "知乎用户"))
        self.user_id.setWhatsThis(_translate("get_user_info_by_uid", "userid"))
        self.user_id.setPlaceholderText(_translate("get_user_info_by_uid", "userid"))
        self.get_uer_following.setText(_translate("get_user_info_by_uid", "用户关注列表"))
        self.get_user_follower.setText(_translate("get_user_info_by_uid", "用户粉丝列表"))
        self.get_user_answers.setText(_translate("get_user_info_by_uid", "用户回答信息"))
        self.get_user_activities.setText(_translate("get_user_info_by_uid", "用户活动信息"))
        self.get_user_info.setText(_translate("get_user_info_by_uid", "用户信息"))
        self.get_user_activity.setText(_translate("get_user_info_by_uid", "用户行为"))
        self.get_user_about.setText(_translate("get_user_info_by_uid", "用户信息"))


class ZhihuOther(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(300)
        self.setupUi()

    def setupUi(self):
        self.ZhiHuOther = QtWidgets.QVBoxLayout(self)
        self.ZhiHuOther.setContentsMargins(0, 0, 0, 0)
        self.ZhiHuOther.setObjectName("ZhiHuOther")

        self.Hot = QtWidgets.QHBoxLayout()
        self.Hot.setObjectName("Hot")
        self.Topic = QtWidgets.QVBoxLayout()
        self.Topic.setObjectName("Topic")
        self.TopicBox = QtWidgets.QHBoxLayout()
        self.TopicBox.setObjectName("TopicBox")
        self.question = QtWidgets.QVBoxLayout()
        self.question.setObjectName("question")
        self.questionBox = QtWidgets.QHBoxLayout()
        self.questionBox.setObjectName("questionBox")

        self.label_hot = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label_hot.setFont(font)
        self.label_hot.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hot.setObjectName("label_hot")

        self.get_hot = PrimaryPushButton(self)
        self.get_hot.setObjectName("get_hot")

        self.label_topic = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label_topic.setFont(font)
        self.label_topic.setAlignment(QtCore.Qt.AlignCenter)
        self.label_topic.setObjectName("label_topic")

        self.Topic_id = LineEdit(self)
        self.Topic_id.setObjectName("Topic_id")

        self.get_topic = PrimaryPushButton(self)
        self.get_topic.setObjectName("get_topic")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.Hot.addWidget(self.label_hot)
        self.Hot.addWidget(self.get_hot)
        self.Hot.setStretch(0, 3)
        self.Hot.setStretch(1, 1)
        self.ZhiHuOther.addLayout(self.Hot)
        self.Topic.addWidget(self.label_topic)
        self.TopicBox.addWidget(self.Topic_id)
        self.TopicBox.addWidget(self.get_topic)
        self.TopicBox.addItem(spacerItem)

        self.TopicBox.setStretch(0, 2)
        self.TopicBox.setStretch(1, 1)
        self.TopicBox.setStretch(2, 2)

        self.Topic.addLayout(self.TopicBox)

        self.Topic.setStretch(0, 2)
        self.Topic.setStretch(1, 1)

        self.label_question = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label_question.setFont(font)
        self.label_question.setAlignment(QtCore.Qt.AlignCenter)
        self.label_question.setObjectName("label_question")

        self.question_id = LineEdit(self)
        self.question_id.setObjectName("question_id")

        self.get_question_answers = PrimaryPushButton(self)
        self.get_question_answers.setObjectName("get_question_answers")

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.ZhiHuOther.addLayout(self.Topic)
        self.question.addWidget(self.label_question)
        self.questionBox.addWidget(self.question_id)
        self.questionBox.addWidget(self.get_question_answers)
        self.questionBox.addItem(spacerItem1)

        self.questionBox.setStretch(0, 2)
        self.questionBox.setStretch(1, 1)
        self.questionBox.setStretch(2, 2)

        self.question.addLayout(self.questionBox)
        self.ZhiHuOther.addLayout(self.question)

        self.ZhiHuOther.setStretch(0, 1)
        self.ZhiHuOther.setStretch(1, 2)
        self.ZhiHuOther.setStretch(2, 2)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_hot.setText(_translate("ZhihuOther", "知乎热搜"))
        self.get_hot.setText(_translate("ZhihuOther", "获取热搜"))
        self.label_topic.setText(_translate("ZhihuOther", "知乎话题"))
        self.Topic_id.setPlaceholderText(_translate("ZhihuOther", "topic_id"))
        self.get_topic.setText(_translate("ZhihuOther", "获取话题相关"))
        self.label_question.setText(_translate("ZhihuOther", "知乎问题回答"))
        self.get_question_answers.setText(_translate("ZhihuOther", "获取所有回答"))


class WeiBo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(300)
        self.setupUi()

    def setupUi(self):
        self.WeiBo = QtWidgets.QVBoxLayout(self)
        self.WeiBo.setContentsMargins(0, 0, 0, 0)
        self.WeiBo.setObjectName("WeiBo")
        self.weibo_user = QtWidgets.QVBoxLayout()
        self.weibo_user.setObjectName("weibo_user")
        self.weibo_hot = QtWidgets.QHBoxLayout()
        self.weibo_hot.setObjectName("weibo_hot")
        self.userBox = QtWidgets.QHBoxLayout()
        self.userBox.setObjectName("userBox")
        self.weiboBox = QtWidgets.QHBoxLayout()
        self.weiboBox.setObjectName("weiboBox")
        self.weibo_content = QtWidgets.QVBoxLayout()
        self.weibo_content.setObjectName("weibo_content")

        self.label_user = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label_user.setFont(font)
        self.label_user.setAlignment(QtCore.Qt.AlignCenter)
        self.label_user.setObjectName("label_user")

        self.use_id = LineEdit(self)
        self.use_id.setClearButtonEnabled(True)
        self.use_id.setObjectName("use_id")

        self.get_user_info = PrimaryPushButton(self)
        self.get_user_info.setObjectName("get_user_info")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.weibo_user.addWidget(self.label_user)
        self.userBox.addWidget(self.use_id)
        self.userBox.addWidget(self.get_user_info)

        self.userBox.addItem(spacerItem)
        self.userBox.setStretch(0, 2)
        self.userBox.setStretch(1, 1)
        self.userBox.setStretch(2, 2)
        self.weibo_user.addLayout(self.userBox)
        self.weibo_user.setStretch(0, 1)
        self.weibo_user.setStretch(1, 1)
        self.WeiBo.addLayout(self.weibo_user)

        self.label_weibo_content = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label_weibo_content.setFont(font)
        self.label_weibo_content.setAlignment(QtCore.Qt.AlignCenter)
        self.label_weibo_content.setObjectName("label_weibo_content")

        self.weibo_id = LineEdit(self)
        self.weibo_id.setClearButtonEnabled(True)
        self.weibo_id.setObjectName("weibo_id")

        self.get_weibo_content = PrimaryPushButton(self)
        self.get_weibo_content.setObjectName("get_weibo_content")

        self.get_weibo_comments = PrimaryPushButton(self)
        self.get_weibo_comments.setObjectName("get_weibo_comments")

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.weibo_content.addWidget(self.label_weibo_content)
        self.weiboBox.addWidget(self.weibo_id)
        self.weiboBox.addWidget(self.get_weibo_content)
        self.weiboBox.addWidget(self.get_weibo_comments)
        self.weiboBox.addItem(spacerItem1)
        self.weiboBox.setStretch(0, 2)
        self.weiboBox.setStretch(1, 1)
        self.weiboBox.setStretch(2, 1)
        self.weiboBox.setStretch(3, 1)
        self.weibo_content.addLayout(self.weiboBox)
        self.weibo_content.setStretch(0, 1)
        self.weibo_content.setStretch(1, 1)
        self.WeiBo.addLayout(self.weibo_content)

        self.label_hot = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label_hot.setFont(font)
        self.label_hot.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hot.setObjectName("label_hot")

        self.get_hot = PrimaryPushButton(self)
        self.get_hot.setObjectName("get_hot")

        self.weibo_hot.addWidget(self.label_hot)
        self.weibo_hot.addWidget(self.get_hot)
        self.weibo_hot.setStretch(0, 3)
        self.weibo_hot.setStretch(1, 1)
        self.WeiBo.addSpacing(30)
        self.WeiBo.addLayout(self.weibo_hot)
        self.WeiBo.setStretch(0, 2)
        self.WeiBo.setStretch(1, 2)
        self.WeiBo.setStretch(2, 2)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_user.setText(_translate("WeiBoBox", "微博用户"))
        self.use_id.setPlaceholderText(_translate("WeiBoBox", "user_id"))
        self.get_user_info.setText(_translate("WeiBoBox", "用户信息"))
        self.label_weibo_content.setText(_translate("WeiBoBox", "微博博文"))
        self.weibo_id.setPlaceholderText(_translate("WeiBoBox", "weibo_id"))
        self.get_weibo_content.setText(_translate("WeiBoBox", "博文信息"))
        self.get_weibo_comments.setText(_translate("WeiBoBox", "微博评论"))
        self.label_hot.setText(_translate("WeiBoBox", "微博热搜"))
        self.get_hot.setText(_translate("WeiBoBox", "获取热搜"))
