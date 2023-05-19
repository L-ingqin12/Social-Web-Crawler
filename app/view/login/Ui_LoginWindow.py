# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1250, 809)
        Form.setMinimumSize(QtCore.QSize(700, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 背景
        self.backgroud = QtWidgets.QLabel(Form)
        self.backgroud.setText("")
        self.backgroud.setPixmap(QtGui.QPixmap(":/images/background.jpg"))
        self.backgroud.setScaledContents(True)
        self.backgroud.setObjectName("label")
        self.horizontalLayout.addWidget(self.backgroud)


        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(360, 0))
        self.widget.setMaximumSize(QtCore.QSize(360, 16777215))
        self.widget.setStyleSheet("QLabel{\n"
                                  "    font: 13px \'Microsoft YaHei\'\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        # 头像
        self.AppHeader = QtWidgets.QLabel(self.widget)
        self.AppHeader.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AppHeader.sizePolicy().hasHeightForWidth())
        self.AppHeader.setSizePolicy(sizePolicy)
        self.AppHeader.setMinimumSize(QtCore.QSize(100, 100))
        self.AppHeader.setMaximumSize(QtCore.QSize(100, 100))
        self.AppHeader.setText("")
        self.AppHeader.setPixmap(QtGui.QPixmap(":/images/logo.png"))
        self.AppHeader.setScaledContents(True)
        self.AppHeader.setObjectName("AppHeader")
        self.verticalLayout_2.addWidget(self.AppHeader, 0, QtCore.Qt.AlignHCenter)


        spacerItem1 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        # self.gridLayout = QtWidgets.QGridLayout()
        # self.gridLayout.setHorizontalSpacing(4)
        # self.gridLayout.setVerticalSpacing(9)
        # self.gridLayout.setObjectName("gridLayout")


        # self.lineEdit = LineEdit(self.widget)
        # self.lineEdit.setClearButtonEnabled(True)
        # self.lineEdit.setObjectName("lineEdit")
        # self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)

        # self.label_3 = QtWidgets.QLabel(self.widget)
        # self.label_3.setObjectName("label_3")
        # self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)


        # self.lineEdit_2 = LineEdit(self.widget)
        # self.lineEdit_2.setPlaceholderText("")
        # self.lineEdit_2.setClearButtonEnabled(True)
        # self.lineEdit_2.setObjectName("lineEdit_2")
        # self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        # self.label_4 = QtWidgets.QLabel(self.widget)
        # self.label_4.setObjectName("label_4")
        # self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        #
        # self.gridLayout.setColumnStretch(0, 2)
        # self.gridLayout.setColumnStretch(1, 1)

        # self.verticalLayout_2.addLayout(self.gridLayout)

        # username
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.username = LineEdit(self.widget)
        self.username.setClearButtonEnabled(True)
        self.username.setObjectName("username")
        self.verticalLayout_2.addWidget(self.username)

        # password
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.password = LineEdit(self.widget)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setClearButtonEnabled(True)
        self.password.setObjectName("password")
        self.verticalLayout_2.addWidget(self.password)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)


        self.rememberMyPassword = CheckBox(self.widget)
        self.rememberMyPassword.setChecked(True)
        self.rememberMyPassword.setObjectName("rememberMyPassword")
        self.verticalLayout_2.addWidget(self.rememberMyPassword)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)


        self.submit = PrimaryPushButton(self.widget)
        self.submit.setObjectName("submit")
        self.verticalLayout_2.addWidget(self.submit)
        spacerItem4 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)

        
        self.pushButton_2 = HyperlinkButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

        # self.lineEdit.setPlaceholderText(_translate("Form", "ftp.example.com"))
        # self.label_3.setText(_translate("Form", "主机"))
        # self.lineEdit_2.setText(_translate("Form", "21"))
        # self.label_4.setText(_translate("Form", "端口"))

        self.label_5.setText(_translate("Form", "用户名"))
        self.username.setPlaceholderText(_translate("Form", "手机号或邮箱"))
        self.label_6.setText(_translate("Form", "密码"))
        self.password.setPlaceholderText(_translate("Form", "••••••••••••"))
        self.rememberMyPassword.setText(_translate("Form", "记住密码"))
        self.submit.setText(_translate("Form", "登录"))
        self.pushButton_2.setText(_translate("Form", "找回密码"))


from qfluentwidgets import CheckBox, HyperlinkButton, LineEdit, PrimaryPushButton
import resource_rc
