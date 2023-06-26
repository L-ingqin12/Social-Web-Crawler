# coding:utf-8
import datetime
import json
import os
import subprocess
from collections import defaultdict

import pymongo
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QPen
from PyQt5.QtWidgets import QGridLayout

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon, LineEdit, InfoBar, InfoBarPosition, DropDownPushButton, \
    Dialog, MessageBox, IndeterminateProgressBar

from .dialog_interface import MyDialog

from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet
from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter)
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from qfluentwidgets import LineEdit, PrimaryPushButton

from ..utils.data_analysis import remove_tags_emojis
from ..utils.lib.weibo_data import WeiboUser, WeiboInfo
from ..utils.lib.zhihu_data import ZhihuUser
from ..utils.mongoDB_operator import MongoDB
from ..utils.weibo import WeiboApi, get_all_comment_weibo, date_format
from ..utils.zhihu import ZhihuApi, get_all_following, user_activities, format_time, get_all_follower, user_all_answers, \
    topic_all_discussions, question_all_answers
import traceback

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

        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub repo'),
            self.tr(
                'Social web crawler captures and analyzes data from Zhihu and Weibo'),
            REPO_URL
        )

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


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.banner = BannerWidget(self)
        self.dataBase = DataBaseWidget(self)
        self.zhihu_user = ZhiHuUser(self)
        self.zhihu_other = ZhihuOther(self)
        self.weibo = WeiBo(self)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.buttonLayout = QHBoxLayout()
        self.scroll_button = ToolButton(FluentIcon.SCROLL, self)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.themeButton, 0, Qt.AlignRight)
        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        self.themeButton.setToolTip(self.tr('切换主题'))
        self.themeButton.clicked.connect(self.toggleTheme)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.scroll_button, 0, Qt.AlignRight)
        self.scroll_button.installEventFilter(ToolTipFilter(self.scroll_button))
        self.scroll_button.setToolTip(self.tr("折叠banner"))
        self.scroll_button.clicked.connect(self.collapse)
        self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.addWidget(self.banner)

        StyleSheet.HOME_INTERFACE.apply(self)

    def collapse(self):
        if self.banner.isHidden():
            self.banner.show()
            self.scroll_button.setToolTip(self.tr("折叠banner"))
        else:
            self.banner.hide()
            self.scroll_button.setToolTip(self.tr("展开banner"))

    def loadSamples(self):
        """ load samples """

        # 将虚线和QSpacerItem添加到每个布局的顶部和底部
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.vBoxLayout.addWidget(self.dataBase)

        self.vBoxLayout.addWidget(line)

        self.vBoxLayout.addWidget(self.zhihu_user)

        self.vBoxLayout.addSpacing(30)

        self.vBoxLayout.addWidget(self.zhihu_other)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        self.vBoxLayout.addWidget(line2)
        self.vBoxLayout.addWidget(self.weibo)
        # self.vBoxLayout.addSpacing(30)
        self.vBoxLayout.addSpacing(100)

    def toggleTheme(self):
        theme = Theme.LIGHT if isDarkTheme() else Theme.DARK
        cfg.set(cfg.themeMode, theme)


class DataBaseWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(280)
        self.label = QLabel(self)
        self.label_2 = QLabel(self.tr("port"), self)

        self.label_3 = QLabel(self.tr("数据库设置"), self)
        self.label_4 = QLabel(self)
        self.setupUi()
        # StyleSheet.HOME_INTERFACE.apply(self)
        # self.setTheme()

    def setupUi(self):
        self.setGeometry(QtCore.QRect(110, 170, 721, 141))
        self.setObjectName("widget")

        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3.setGeometry(QtCore.QRect(110, 40, 731, 25))
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.setGeometry(QtCore.QRect(110, 90, 741, 155))

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

        self.database_returnword = LineEdit(self)
        self.database_returnword.setObjectName("database_returnword")
        self.database_returnword.setPlaceholderText("admin|None")
        self.database_returnword.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.database_returnword, 2, 3, 1, 1)

        self.database_dbname = LineEdit(self)
        self.database_dbname.setObjectName("database_dbname")
        self.database_dbname.setPlaceholderText("mydb")
        self.database_dbname.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.database_dbname, 2, 4, 1, 1)

        self.submit = PrimaryPushButton(self)
        self.submit.setObjectName("submit")
        self.gridLayout.addWidget(self.submit, 3, 2, 1, 1)
        self.submit.clicked.connect(self.connect_database)

        self.export_data = PrimaryPushButton(self)
        self.export_data.setText("导出数据库")
        self.export_data.setEnabled(False)
        self.export_data.clicked.connect(self.export_data_)
        self.gridLayout.addWidget(self.export_data, 4, 2, 1, 1)

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
        try:
            database_url = self.database_url.text()
            port = int(self.database_port.text()) if self.database_port.text() else None

            username = self.database_username.text()
            password = self.database_returnword.text()
            db_name = self.database_dbname.text()
            if len(database_url) == 0 or port is None or port <= 0 or len(db_name) == 0:
                InfoBar.error(
                    title="error",
                    content="please enter your database_url and port and dbname",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=2000,  # won't disappear automatically -1
                    parent=self
                )
                return
            try:
                if len(username) == 0 and len(password) == 0:
                    print("connect database by username and password")
                    mongodb = MongoDB(host=database_url, port=port, db_name=db_name, username=username,
                                      password=password)

                else:
                    print("connect database without password and username")
                    mongodb = MongoDB(host=database_url, port=port, db_name=db_name)
                # print(mongodb)
                InfoBar.success(
                    title="success",
                    content="数据库连接成功",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
                self.export_data.setEnabled(True)
            except Exception as e:
                print("Traceback", e)
                traceback.print_exc()
                return
        except Exception as e:
            print("Traceback", e)
            traceback.print_exc()
            InfoBar.error(
                title="error",
                content=e,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return

    def export_data_(self):
        print("export_data beginning")
        try:
            if mongodb != None:
                mongo_uri = f"mongodb://{self.database_url.text()}:{self.database_port.text()}/"
                dbname = self.database_dbname.text()

                # 连接MongoDB数据库
                client = pymongo.MongoClient(mongo_uri)
                db = client[dbname]
                collections = db.list_collection_names()

                # 导出每个collection的数据为JSON文件
                for collection_name in collections:
                    # 查询collection中的所有文档
                    # print(collection_name,type(collection_name))
                    # collection = db[collection_name]
                    # documents = collection.find()
                    # print(documents)
                    # print(type(documents))
                    # 将文档数据写入JSON文件
                    documents = mongodb.export_data(collection_name=collection_name)
                    # print(documents)
                    filename = f"trash\\{collection_name}.json"
                    with open(filename, "w", encoding='utf-8') as file:
                        for document in documents:
                            file.write(str(document))
                            file.write("\n")

                    print(f"Collection '{collection_name}' 导出为 {filename}")

                current_dir = os.path.dirname(os.path.abspath(__file__))
                root_dir = os.path.abspath(os.path.join(current_dir, '..\..'))
                folder_path = os.path.join(root_dir, "trash")
                subprocess.Popen(f'explorer {folder_path}')
        except Exception as e:
            print("Traceback :", e)
            traceback.print_exc()


class ZhiHuUser(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(200)
        self.setupUi()
        self.binding_button_click()

        # self.setTheme()
        StyleSheet.HOME_INTERFACE.apply(self)

    def setupUi(self):
        self.zhihu_user = QtWidgets.QVBoxLayout(self)
        self.zhihu_user.setContentsMargins(0, 0, 0, 0)
        self.zhihu_user.setObjectName("zhihu_user")
        self.info = QtWidgets.QHBoxLayout()
        self.info.setObjectName("info")
        self.buttonGroup = QtWidgets.QFormLayout()
        self.buttonGroup.setObjectName("buttonGroup")

        self.label = QtWidgets.QLabel(self.tr("知乎用户"), self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.user_id = LineEdit(self)
        self.user_id.setText("")
        self.user_id.setClearButtonEnabled(True)
        self.user_id.setObjectName("user_id")

        self.get_uer_following = PrimaryPushButton(self)
        # self.get_uer_following.setStyleSheet('''''')
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

    def binding_button_click(self):
        # self.get_user_info.click()
        self.get_user_info.clicked.connect(self.user_info)
        self.get_uer_following.clicked.connect(self.user_following)
        self.get_user_answers.clicked.connect(self.user_answers)
        self.get_user_activities.clicked.connect(self.user_activities)
        self.get_user_follower.clicked.connect(self.user_follower)

    def user_info(self):
        user_id = self.user_id.text()
        if len(user_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写user_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )
        api = ZhihuApi()
        data = api.get_user_profile(user_id)
        print(data)
        if 'error' in data:
            InfoBar.error(
                title="error",
                content="未获取到数据",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=1000,
                parent=self
            )
        else:
            self.showDialog(data=data, user_id=user_id)
        return

    def user_following(self):
        user_id = self.user_id.text()
        if len(user_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写user_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            users = get_all_following(user_id=user_id)
            data = []
            for user in users:
                item = {}
                item['url_token'] = user['url_token']
                item['name'] = user['name']
                gender = user['gender']
                if gender == 0:
                    gender = 'undefined'
                elif gender == 1:
                    gender = 'male'
                elif gender == 2:
                    gender = 'female'
                else:
                    gender = "unknown"
                item['gender'] = gender
                item['follower_count'] = user['follower_count']
                item['answer_count'] = user['answer_count']
                data.append(item)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            # dialog.resize(500, 700)
            dialog.timeline_analysis.setHidden(True)
            dialog.gender_analysis.setHidden(True)
            dialog.city_hot.setHidden(True)
            dialog.wordcloud.setHidden(True)
            dialog.show_label.setHidden(True)
            dialog.gridLayout.setColumnStretch(0, 2)
            dialog.gridLayout.setColumnStretch(1, 2)
            dialog.gridLayout.setColumnStretch(2, 0)
            dialog.gridLayout.setColumnStretch(3, 0)

            if dialog.exec():
                try:
                    exist_data = mongodb.find_one(collection_name='user',
                                                  filter={'type': "following", 'user_id': user_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="user",
                                           document={'type': "following", 'user_id': user_id, 'data': users})
                    else:
                        mongodb.update_one(collection_name="user", filter={'type': "following", 'user_id': user_id},
                                           update={'$set': {'data': users}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            return
        return

    def user_answers(self):
        user_id = self.user_id.text()
        if len(user_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写user_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            answers = user_all_answers(user_id)
            data = []
            for answer in answers:
                item = {}
                item['id'] = answer['id']
                item['created_time'] = format_time(answer['created_time'])
                item['voteup_count'] = answer['voteup_count']
                item['answer_type'] = answer['answer_type']
                item['excerpt'] = answer['excerpt']

                data.append(item)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            dialog.timeline_analysis.setHidden(True)
            dialog.gender_analysis.setHidden(True)
            dialog.city_hot.setHidden(True)
            dialog.wordcloud.setHidden(True)
            dialog.show_label.setHidden(True)
            dialog.gridLayout.setColumnStretch(0, 2)
            dialog.gridLayout.setColumnStretch(1, 2)
            dialog.gridLayout.setColumnStretch(2, 0)
            dialog.gridLayout.setColumnStretch(3, 0)

            if dialog.exec():
                try:
                    exist_data = mongodb.find_one(collection_name='user', filter={'type': "answer", 'user_id': user_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="user",
                                           document={'type': "answer", 'user_id': user_id, 'data': answers})
                    else:
                        mongodb.update_one(collection_name="user", filter={'type': "answer", 'user_id': user_id},
                                           update={'$set': {'data': answers}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            return
        return

    def user_activities(self):
        user_id = self.user_id.text()
        if len(user_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写user_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            activities = user_activities(user_id)
            print(activities)
            data = []
            for activitie in activities:
                item = {}
                item['created_time'] = format_time(activitie['created_time'])
                item['action_text'] = activitie['action_text']
                if activitie['action_text'] == "回答了问题" or activitie['action_text'] == "赞同了回答" or activitie[
                    'action_text'] == '收藏了回答':
                    item['theme'] = activitie['target']['question']['title']
                elif activitie['action_text'] == "赞同了文章" or activitie['action_text'] == "关注了问题" or activitie[
                    'action_text'] == '收藏了文章' or activitie['action_text'] == '发表了文章' or activitie[
                    'action_text'] == '添加了问题':
                    item['theme'] = activitie['target']['title']
                # elif activitie['action_text']=="赞同了回答":
                elif "关注了" in activitie['action_text']:
                    if "话题" not in activitie['action_text'] and "问题" not in activitie['action_text']:
                        item['theme'] = activitie['target']['name']
                elif "发布了想法" == activitie['action_text']:
                    item['theme'] = activitie['target']['content'][0]['content']
                else:
                    item['theme'] = activitie['target']

                data.append(item)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            # dialog.resize(500, 700)
            dialog.timeline_analysis.setHidden(True)
            dialog.gender_analysis.setHidden(True)
            dialog.city_hot.setHidden(True)
            dialog.wordcloud.setHidden(True)
            dialog.show_label.setHidden(True)
            dialog.gridLayout.setColumnStretch(0, 2)
            dialog.gridLayout.setColumnStretch(1, 2)
            dialog.gridLayout.setColumnStretch(2, 0)
            dialog.gridLayout.setColumnStretch(3, 0)

            if dialog.exec():
                try:
                    exist_data = mongodb.find_one(collection_name='user',
                                                  filter={"type": "activity", 'user_id': user_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="user",
                                           document={"type": "activity", 'user_id': user_id, 'data': activities})
                    else:
                        mongodb.update_one(collection_name="user", filter={"type": "activity", 'user_id': user_id},
                                           update={'$set': {'data': activities}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            return

        return

    def user_follower(self):
        user_id = self.user_id.text()
        if len(user_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写user_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            users = get_all_follower(user_id=user_id)
            data = []
            for user in users:
                item = {}
                item['url_token'] = user['url_token']
                item['name'] = user['name']
                gender = user['gender']
                if gender == 0:
                    gender = 'undefined'
                elif gender == 1:
                    gender = 'male'
                elif gender == 2:
                    gender = 'female'
                else:
                    gender = "unknown"
                item['gender'] = gender

                item['follower_count'] = user['follower_count']
                item['answer_count'] = user['answer_count']
                data.append(item)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            dialog.timeline_analysis.setHidden(True)
            dialog.city_hot.setHidden(True)
            dialog.wordcloud.setHidden(True)
            dialog.gridLayout.setRowStretch(0, 0)
            dialog.gridLayout.setRowStretch(1, 0)
            dialog.gridLayout.setRowStretch(2, 2)
            dialog.gridLayout.setRowStretch(3, 0)
            dialog.gridLayout.setRowStretch(4, 1)

            if dialog.exec():
                try:
                    exist_data = mongodb.find_one(collection_name='user',
                                                  filter={"type": "follower", 'user_id': user_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="user",
                                           document={'type': "follower", 'user_id': user_id, 'data': users})
                    else:
                        mongodb.update_one(collection_name="user", filter={"type": "follower", 'user_id': user_id},
                                           update={'$set': {'data': users}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            return
        return

    def showDialog(self, data, user_id):
        title = self.tr(f'{user_id}的用户信息')
        info = data
        user = ZhihuUser(user_id=user_id, name=info["name"], gender=info["gender"],
                         following=info["following_count"],
                         follower=info["follower_count"], description=info["description"],
                         answer_count=info["answer_count"],
                         articles_count=info["articles_count"], ip_info=info["ip_info"],
                         thank_count=info["thanked_count"],
                         type=info["type"], voteup_count=info["voteup_count"], headline=info["headline"],
                         following_favlists_count=info["following_favlists_count"],
                         following_question_count=info["following_question_count"],
                         following_topic_count=info["following_topic_count"],
                         following_columns_count=info["following_columns_count"],
                         question_count=info["question_count"],
                         pins_count=info["pins_count"], favorite_count=info["favorite_count"],
                         favorited_count=info["favorited_count"])

        content = self.tr(user.list_all_members())
        w = MessageBox(title, content, self.window())
        w.yesButton.setText("保存至数据库")
        w.cancelButton.setText("退出")
        if mongodb is None:
            w.yesButton.setEnabled(False)
            w.yesButton.setToolTip("请配置数据库后重新尝试！")
        # layout = QVBoxLayout(w)
        #
        # buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # buttonBox.button(QDialogButtonBox.Ok).setText("保存至数据库")
        # buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        # layout.addWidget(buttonBox)
        # w.exec_()
        # button = QAction(self.tr('Action'))
        #
        # if mongodb == None:
        #     button.setEnabled(False)
        #     button.setToolTip("请配置数据库后重新尝试！")
        # else:
        #     button.triggered.connect(lambda: mongodb.insert(collection_name="zhihu_user_info", document={'user_id': user_id, 'data': data}))
        # w.addAction(button)

        if w.exec():
            # self.tips_for_save_data(collection_name="zhihu_user_info", document={'user_id': user_id, 'data': data})
            try:
                exist_data = mongodb.find_one(collection_name='user_info',
                                              filter={'source': "zhihu", 'user_id': user_id})
                if exist_data:
                    mongodb.insert_one(collection_name="user_info",
                                       document={'source': "zhihu", 'user_id': user_id, 'data': data})
                else:
                    mongodb.update_one(collection_name="user_info", filter={'source': "zhihu", 'user_id': user_id},
                                       update={'$set': {'data': data}})
                InfoBar.success(
                    title="success",
                    content="数据保存成功！",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
            except Exception as e:
                InfoBar.error(
                    title="error",
                    content=e,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=2000,  # won't disappear automatically -1
                    parent=self
                )
            print("Yes button is clicked")
        else:
            print('Cancel button is pressed')


class ZhihuOther(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(300)
        self.setupUi()
        self.binding_button_click()

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

        self.answer_id = LineEdit(self)
        self.answer_id.setObjectName("answer_id")

        self.get_zhihu_comments = PrimaryPushButton(self)
        self.get_zhihu_comments.setObjectName("get_zhihu_comments")

        # spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.ZhiHuOther.addLayout(self.Topic)
        self.question.addWidget(self.label_question)
        self.questionBox.addWidget(self.question_id)
        self.questionBox.addWidget(self.get_question_answers)
        self.questionBox.addWidget(self.answer_id)
        self.questionBox.addWidget(self.get_zhihu_comments)
        # self.questionBox.addItem(spacerItem1)

        self.questionBox.setStretch(0, 3)
        self.questionBox.setStretch(1, 2)
        self.questionBox.setStretch(2, 2)
        self.questionBox.setStretch(3, 1)
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
        self.question_id.setPlaceholderText(_translate("ZhihuOther", "question_id"))
        self.get_question_answers.setText(_translate("ZhihuOther", "获取所有回答"))
        self.answer_id.setPlaceholderText(_translate("ZhihuOther", "answer_id"))
        self.get_zhihu_comments.setText(_translate("ZhihuOther", "获取所有评论"))

    def binding_button_click(self):
        self.get_hot.clicked.connect(self._get_hot)
        self.get_topic.clicked.connect(self._get_topic)
        self.get_question_answers.clicked.connect(self._get_question_answer)
        self.get_zhihu_comments.clicked.connect(self._get_zhihu_comments)

    def _get_hot(self):
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            zhihu = ZhihuApi()
            json = zhihu.get_hotlist()['data']
            data = []
            for hot in json:
                item = {}
                info = hot['target']
                item['created_time'] = format_time(hot['created_time'])[10:]
                item['title'] = remove_tags_emojis(info['question']['title'])[:15] + '...' if len(
                    remove_tags_emojis(info['question']['title'])) > 15 else remove_tags_emojis(
                    info['question']['title'])
                item['id'] = info['id']
                item['answer_count'] = info["question"]['answer_count']
                item['url_token'] = info['author']['url_token'] if info['author']['name'] != '匿名用户' else ''
                item['name'] = info['author']['name']
                data.append(item)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            # dialog.resize(500, 700)
            dialog.timeline_analysis.setHidden(True)
            dialog.gender_analysis.setHidden(True)
            dialog.city_hot.setHidden(True)
            dialog.wordcloud.setHidden(True)
            dialog.show_label.setHidden(True)
            dialog.gridLayout.setColumnStretch(0, 2)
            dialog.gridLayout.setColumnStretch(1, 2)
            dialog.gridLayout.setColumnStretch(2, 0)
            dialog.gridLayout.setColumnStretch(3, 0)

            if dialog.exec():
                try:
                    exist_data = mongodb.find_one(collection_name="hot_info",
                                                  filter={'source': "zhihu", 'time': datetime.datetime.now()})
                    if exist_data:
                        mongodb.insert_one(collection_name="hot_info",
                                           document={'source': "zhihu", 'time': datetime.datetime.now(), 'data': json})
                    else:
                        mongodb.update_one(collection_name="hot_info",
                                           filter={'source': "zhihu", 'time': datetime.datetime.now()},
                                           update={'$set': {'data': json}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            return
        return

    def _get_topic(self):
        topic_id = self.Topic_id.text()
        if len(topic_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写topic_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            discussions = topic_all_discussions(topic_id=topic_id)
            data = []
            for discussion in discussions:
                print(discussion)
                item = {}
                target = discussion['target']
                item['id'] = target['id']
                item['created_time'] = target['created_time'] if 'created_time' in target else ''
                item['comment_count'] = target['comment_count'] if 'comment_count' in target else ''
                item['favlists_count'] = target['favlists_count'] if 'favlists_count' in target else ''
                item['author'] = target['author']['name'] if 'author' in target else ""
                item['user_id'] = target['author']['url_token'] if 'author' in target else ''
                item['excerpt'] = remove_tags_emojis(target['excerpt']) if 'excerpt' in target else ''
                gender = target['author']['gender'] if 'author' in target else -1
                if gender == 0:
                    gender = 'undefined'
                elif gender == 1:
                    gender = 'male'
                elif gender == 2:
                    gender = 'female'
                else:
                    gender = "unknown"
                item['gender'] = gender
                data.append(item)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            # dialog.resize(500, 700)
            dialog.timeline_analysis.setHidden(True)
            # dialog.gender_analysis.setHidden(True)
            dialog.city_hot.setHidden(True)
            dialog.wordcloud.setHidden(True)
            # dialog.show_label.setHidden(True)
            # dialog.gridLayout.setColumnStretch(0, 2)
            # dialog.gridLayout.setColumnStretch(1, 2)
            # dialog.gridLayout.setColumnStretch(2, 0)
            # dialog.gridLayout.setColumnStretch(3, 0)

            if dialog.exec():
                try:
                    exist_data = mongodb.find_one(collection_name="topic_discussions",
                                                  filter={'topic_id': topic_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="topic_discussions",
                                           document={'topic_id': topic_id, 'data': discussions})
                    else:
                        mongodb.update_one(collection_name="hot_info", filter={'topic_id': topic_id},
                                           update={'$set': {'data': discussions}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            return
        return

    def _get_question_answer(self):
        question_id = self.question_id.text()
        if len(question_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写question_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            answers = question_all_answers(question_id)
            data = []
            for answer in answers:
                item = {}
                item['id'] = answer['id']
                item['created_time'] = format_time(answer['created_time'])
                item['voteup_count'] = answer['voteup_count']
                item['answer_type'] = answer['answer_type']
                item['excerpt'] = answer['excerpt']

                data.append(item)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            dialog.timeline_analysis.setHidden(True)
            dialog.gender_analysis.setHidden(True)
            dialog.city_hot.setHidden(True)
            dialog.wordcloud.setHidden(True)
            dialog.show_label.setHidden(True)
            dialog.gridLayout.setColumnStretch(0, 2)
            dialog.gridLayout.setColumnStretch(1, 2)
            dialog.gridLayout.setColumnStretch(2, 0)
            dialog.gridLayout.setColumnStretch(3, 0)

            if dialog.exec():
                try:
                    exist_data = mongodb.find_one(collection_name="question_answers",
                                                  filter={'question_id': question_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="question_answers",
                                           document={'question_id': question_id, 'data': answers})
                    else:
                        mongodb.update_one(collection_name="hot_info", filter={'question_id': question_id},
                                           update={'$set': {'data': answers}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            return
        return

    def _get_zhihu_comments(self):
        question_id = self.question_id.text()
        answer_id = self.answer_id.text()
        if len(question_id) == 0 or len(answer_id) == 0:
            # print(1)
            #
            InfoBar.error(
                title="error",
                content="请填写question_id|answer_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            api = ZhihuApi()
            review_answers = api.get_answer_reviews(answer_id=answer_id, question_id=question_id)
            data = []
            for review_answer in review_answers:
                item = {}
                item['created_time'] = format_time(review_answer['created_time'])

                comment_tag = review_answer['comment_tag']
                print(comment_tag)
                if len(comment_tag) >= 1:
                    item['ip'] = comment_tag[0]['text'].replace('IP 属地', '') if comment_tag[0][
                                                                                  'type'] == 'ip_info' else "未识别"
                author = review_answer['author']
                gender = author['gender']
                if gender == 0:
                    gender = 'undefined'
                elif gender == 1:
                    gender = 'male'
                elif gender == 2:
                    gender = 'female'
                else:
                    gender = "unknown"
                item['gender'] = gender
                item['user_id'] = author['url_token']
                item['user_name'] = author['name']
                item['user_info'] = author['headline']  # 个人简介
                item['user_type'] = author['type']
                item['content'] = remove_tags_emojis(review_answer['content'])
                data.append(item)
            # print(review_answers)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            if dialog.exec():
                try:
                    exist_data = mongodb.find_one(collection_name="comments",
                                                  filter={'source': "zhihu_answer", 'question_id': question_id,
                                                          'answer_id': answer_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="comments",
                                           document={'source': "zhihu_answer", 'question_id': question_id,
                                                     'answer_id': answer_id,
                                                     'data': review_answers})
                    else:
                        mongodb.update_one(collection_name="hot_info",
                                           filter={'source': "zhihu_answer", 'question_id': question_id,
                                                   'answer_id': answer_id},
                                           update={'$set': {'data': review_answers}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            traceback.print_exc()
            return
        return


class WeiBo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(300)
        self.setupUi()
        self.binding_button_click()

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

    def binding_button_click(self):
        self.get_hot.clicked.connect(self._get_hot)
        self.get_user_info.clicked.connect(self._get_user_info)
        self.get_weibo_content.clicked.connect(self._get_weibo_content)
        self.get_weibo_comments.clicked.connect(self._get_weibo_comments)

    def _get_hot(self):
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            weibo = WeiboApi()
            json = weibo.get_hot()
            if json['ok'] == 1:
                data = json['data']['cards'][0]['card_group']
                dialog = MyDialog(db=mongodb, data=data, headers=['desc', 'desc_extr'], parent=self)
                dialog.rows = 50
                dialog.resize(500, 700)
                dialog.timeline_analysis.setHidden(True)
                dialog.gender_analysis.setHidden(True)
                dialog.city_hot.setHidden(True)
                dialog.wordcloud.setHidden(True)
                dialog.show_label.setHidden(True)
                dialog.gridLayout.setColumnStretch(0, 2)
                dialog.gridLayout.setColumnStretch(1, 2)
                dialog.gridLayout.setColumnStretch(2, 0)
                dialog.gridLayout.setColumnStretch(3, 0)
                if dialog.exec():
                    try:

                        exist_data = mongodb.find_one(collection_name="hot_info",
                                                      filter={'source': 'weibo', 'time': datetime.datetime.now()})
                        if exist_data:
                            mongodb.insert_one(collection_name="hot_info",
                                               document={'source': 'weibo', 'time': datetime.datetime.now(),
                                                         'data': data})
                        else:
                            mongodb.update_one(collection_name="hot_info",
                                               filter={'source': 'weibo', 'time': datetime.datetime.now()},
                                               update={'$set': {'data': data}})
                        InfoBar.success(
                            title="success",
                            content="数据保存成功！",
                            orient=Qt.Horizontal,
                            isClosable=True,
                            position=InfoBarPosition.TOP,
                            duration=2000,
                            parent=self
                        )
                    except Exception as e:
                        InfoBar.error(
                            title="error",
                            content=e,
                            orient=Qt.Horizontal,
                            isClosable=True,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            duration=2000,  # won't disappear automatically -1
                            parent=self
                        )
                    print("Yes button clicked")
                else:
                    print("Cancel button clicked")
                print(data)
        except Exception as e:
            print('Traceback:', e)
            return
        # dialog = MyDialog(db=mongodb,data=data)
        return

    def _get_user_info(self):
        user_id = self.use_id.text()
        if len(user_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写user_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        weibo = WeiboApi()
        data = weibo.get_user(uid=user_id)
        print(data)
        self.showDialog(data=data, user_id=user_id)
        return

    def _get_weibo_content(self):
        weibo_id = self.weibo_id.text()
        if len(weibo_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写weibo_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        try:
            weibo = WeiboApi()
            data = weibo.get_weibo_info(weibo_id=weibo_id)['status']
            info = WeiboInfo()
            info.id = data['id']
            info.publish_tool = data['source']
            info.publish_place = data['region_name']
            info.publish_time = date_format(data['created_at'])
            info.content = remove_tags_emojis(data['text'])
            info.user_id = data['user']['id']
            info.comment_num = data['comments_count']
            info.retweet_num = data['reposts_count']
            info.up_num = data['attitudes_count']
            print(info.list_all_members())
            w = MessageBox(title=f"{weibo_id}的博文内容", content=info.list_all_members(), parent=self.window())
            w.yesButton.setText("保存至数据库")
            w.cancelButton.setText("退出")
            if mongodb is None:
                w.yesButton.setEnabled(False)
                w.yesButton.setToolTip("请配置数据库后重新尝试！")
            if w.exec():
                try:
                    exist_data = mongodb.find_one(collection_name="weibo_content",
                                                  filter={'weibo_id': weibo_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="weibo_content",
                                           document={'weibo_id': weibo_id, 'data': data})
                    else:
                        mongodb.update_one(collection_name="weibo_content",
                                           filter={'weibo_id': weibo_id},
                                           update={'$set': {'data': data}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button is clicked")
            else:
                print("Cancel button  clicked")
        except Exception as e:
            print('Traceback:', e)
            traceback.print_exc()
            return
        return

    def _get_weibo_comments(self):
        weibo_id = self.weibo_id.text()
        if len(weibo_id) == 0:
            InfoBar.error(
                title="error",
                content="请填写weibo_id后重试",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.NONE,
                duration=2000,  # won't disappear automatically -1
                parent=self
            )
            return
        InfoBar.success(
            title="success",
            content="正在获取数据请稍后...",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        # InfoBar.show(self)
        try:
            comments = get_all_comment_weibo(weibo_id)
            data = []
            for comment in comments:
                item = {}
                item['id'] = comment['id']
                item['created_time'] = date_format(comment['created_at'])

                item['ip'] = comment['source'].replace('来自', '')
                # item['user'] = comment['user']
                item['user_id'] = comment['user']['id']
                item['name'] = comment['user']['screen_name']
                item['gender'] = 'female' if comment['user']['gender'] == 'f' else 'male'
                item['description'] = comment['user']['description']

                item['content'] = remove_tags_emojis(comment['text'])
                data.append(item)
            if not data:
                InfoBar.error(
                    title="error",
                    content="未获取到数据",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.NONE,
                    duration=1000,
                    parent=self
                )
                return
            dialog = MyDialog(db=mongodb, data=data, headers=[key for key in data[0].keys()], parent=self)
            if dialog.exec():
                try:

                    exist_data = mongodb.find_one(collection_name="comments",
                                                  filter={'source': 'weibo', 'weibo_id': weibo_id})
                    if exist_data:
                        mongodb.insert_one(collection_name="comments",
                                           document={'source': 'weibo', 'weibo_id': weibo_id,
                                                     'data': comments})
                    else:
                        mongodb.update_one(collection_name="comments",
                                           filter={'source': 'weibo', 'weibo_id': weibo_id},
                                           update={'$set': {'data': comments}})
                    InfoBar.success(
                        title="success",
                        content="数据保存成功！",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                except Exception as e:
                    InfoBar.error(
                        title="error",
                        content=e,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,  # won't disappear automatically -1
                        parent=self
                    )
                print("Yes button clicked")
            else:
                print("Cancel button clicked")
            print(data)
        except Exception as e:
            print('Traceback:', e)
            traceback.print_exc()
            return
        return

    def showDialog(self, data, user_id):
        title = self.tr(f'{user_id}的用户信息')
        if data['ok'] != 1:
            return
        info = data['data']['userInfo']
        try:
            user = WeiboUser(id=info['id'], nickname=info['screen_name'], gender=info['gender'],
                             description=info['description'],
                             verified_reason=info['verified_reason'] if info['verified'] else None,
                             weibo_num=info['statuses_count'], following=info['follow_count'],
                             followers=info['followers_count'])
            content = self.tr(user.list_all_members())
            w = MessageBox(title, content, self.window())
            w.yesButton.setText("保存至数据库")
            w.cancelButton.setText("退出")
            if mongodb is None:
                w.yesButton.setEnabled(False)
                w.yesButton.setToolTip("请配置数据库后重新尝试！")
        except Exception as e:
            print("Error", e)
            return

        if w.exec():
            try:

                exist_data = mongodb.find_one(collection_name="user_info",
                                              filter={'source': "weibo", 'user_id': user_id})
                if exist_data:
                    mongodb.insert_one(collection_name="user_info",
                                       document={'source': "weibo", 'user_id': user_id, 'data': info})
                else:
                    mongodb.update_one(collection_name="user_info",
                                       filter={'source': "weibo", 'user_id': user_id},
                                       update={'$set': {'data': info}})
                InfoBar.success(
                    title="success",
                    content="数据保存成功！",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
            except Exception as e:
                InfoBar.error(
                    title="error",
                    content=e,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=2000,  # won't disappear automatically -1
                    parent=self
                )
            print("Yes button is clicked")
        else:
            print('Cancel button is pressed')
        return
