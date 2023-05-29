from collections import defaultdict

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QWidget, QVBoxLayout
from qfluentwidgets import PixmapLabel, PrimaryPushButton, TableWidget, InfoBar, InfoBarPosition, ToolButton, FluentIcon

import traceback

from app.utils.data_analysis import create_wordcloud, gender_analysis, create_city_hot, time_line_analysis


class MyDialog(QDialog):
    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, headers, data, db, parent=None):
        super().__init__(parent=parent)
        self.headers = headers
        self.data = data
        self.db = db
        self.cols = len(self.headers)
        print(len(self.data))
        self.rows = len(self.data)
        self.setupUi()
        self.binding_click_button()
        self.width=410
        self.height=400

    def setupUi(self):
        self.resize(960, 700)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.table = TableWidget(self)
        self.table.setObjectName("table")

        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(len(self.data))
        self.load_data()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        # self.table.setColumnWidth(len(self.headers)-1, 400)
        # self.setColumnWidth(1, 600)

        # 设置header宽度
        # header = self.horizontalHeader()
        # header.setSectionResizeMode(0, header.ResizeToContents)
        # header.setSectionResizeMode(1, header.Stretch)
        self.table.setWordWrap(True)
        self.gridLayout.addWidget(self.table, 0, 0, 4, 2)

        self.wordcloud = PrimaryPushButton(self)
        self.wordcloud.setObjectName("wordcloud")
        self.gridLayout.addWidget(self.wordcloud, 0, 2, 1, 1)

        self.timeline_analysis = PrimaryPushButton(self)
        self.timeline_analysis.setObjectName("timeline_analysis")
        self.gridLayout.addWidget(self.timeline_analysis, 1, 2, 1, 1)

        self.gender_analysis = PrimaryPushButton(self)
        self.gender_analysis.setObjectName("gender_analysis")
        self.gridLayout.addWidget(self.gender_analysis, 2, 2, 1, 1)

        self.city_hot = PrimaryPushButton(self)
        self.city_hot.setObjectName("city_hot")
        self.gridLayout.addWidget(self.city_hot, 3, 2, 1, 1)

        self.save_to_database = PrimaryPushButton(self)
        self.save_to_database.setObjectName("save_to_database")
        self.gridLayout.addWidget(self.save_to_database, 4, 0, 1, 1)

        self.cancle = PrimaryPushButton(self)
        self.cancle.setObjectName("cancle")
        self.gridLayout.addWidget(self.cancle, 4, 1, 1, 1)

        self.show_label = PixmapLabel(self)
        self.show_label.setObjectName("show_label")
        self.gridLayout.addWidget(self.show_label, 0, 3, 4, 1)

        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 6)
        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(2, 2)
        self.gridLayout.setRowStretch(3, 2)
        self.gridLayout.setRowStretch(4, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.wordcloud.setText(_translate("self", "词云分析"))
        self.timeline_analysis.setText(_translate("self", "时间线统计"))
        self.gender_analysis.setText(_translate("self", "性别比例分析"))
        self.city_hot.setText(_translate("self", "城市热力图"))
        self.save_to_database.setText(_translate("self", "保存到数据库"))
        self.cancle.setText(_translate("self", "退出"))

    def load_data(self):

        self.table.setHorizontalHeaderLabels(self.headers)
        for i in range(self.rows):
            row = self.data[i]
            for j in range(self.cols):
                Item = QTableWidgetItem(str(row[self.headers[j]]) if self.headers[j] in row else '')
                Item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, j, Item)

    def binding_click_button(self):
        self.wordcloud.clicked.connect(self._wordcloud)
        self.gender_analysis.clicked.connect(self._gender_analysis)
        self.city_hot.clicked.connect(self._city_hot)
        self.timeline_analysis.clicked.connect(self._timeline_analysis)
        if self.db != None:
            self.save_to_database.clicked.connect(self._save_to_database)
        else:
            self.save_to_database.setEnabled(False)
        self.cancle.clicked.connect(self._cancle)

    def _wordcloud(self):
        context = ''
        for i in self.data:
            if 'content' in i:
                context += i['content']
        try:
            create_wordcloud(context)
            self.show_label.clear()
            pixmap = QPixmap('trash/wordcloud.jpg')
            scaled_pixmap = pixmap.scaled(self.show_label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            # print(self.show_label.size().width(),self.show_label.size().height())
            self.show_label.setPixmap(scaled_pixmap)
            self.show_label.setFixedSize(self.width, self.height)
        except Exception as e:
            print("Traceback", e)
            traceback.print_exc()
            return
        return

    def _gender_analysis(self):
        gender_count = defaultdict(int)
        for i in self.data:
            if 'gender' in i:
                gender_count[i['gender']] += 1
        gender_count = dict(gender_count)
        try:
            gender_analysis(gender_count)
            self.show_label.clear()
            pixmap = QPixmap('trash/gender_analysis.png')
            scaled_pixmap = pixmap.scaled(self.show_label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            self.show_label.setPixmap(scaled_pixmap)
            self.show_label.setFixedSize(self.width,self.height)
        except Exception as e:
            print("Traceback", e)
            traceback.print_exc()
        return

    def _city_hot(self):
        city_count = defaultdict(int)
        for i in self.data:
            if 'ip' in i:
                city_count[i['ip']] += 1
        city_count = dict(city_count)
        try:
            create_city_hot(city_count)
            widget = CityWidget(self)
            widget.resize(1000, 600)
            widget.show()
        except Exception as e:
            print("Traceback",e)
            traceback.print_exc()
            return
        return

    def _timeline_analysis(self):
        time_list = []
        for i in self.data:
            if 'created_time' in i:
                time_list.append(i['created_time'])
        try:
            time_line_analysis(time_list)
            self.show_label.clear()
            pixmap = QPixmap('trash/time_line_analysis.png')
            scaled_pixmap = pixmap.scaled(self.show_label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            self.show_label.setPixmap(scaled_pixmap)
            self.show_label.setFixedSize(self.width, self.height)
        except Exception as e:
            print("Traceback", e)
            traceback.print_exc()
            return
        return

    def _save_to_database(self):
        self.accept()
        self.yesSignal.emit()
        return

    def _cancle(self):
        self.reject()
        self.cancelSignal.emit()
        return


class CityWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("社交网络爬虫")
        # 创建QWebEngineView实例
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.webview = QWebEngineView(self)

        # 加载包含JavaScript代码的HTML页面
        html = open("trash/city_heat_map.html", encoding='utf-8').read()
        self.webview.setHtml(html)

        # 将QWebEngineView添加到QWidget中
        self.layout = QVBoxLayout(self)
        # self.close_button = ToolButton(FluentIcon.CLOSE, self)
        # self.layout.addWidget(self.close_button, 0, Qt.AlignRight)
        # self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.webview)
