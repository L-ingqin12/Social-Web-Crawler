# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(978, 640)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(120, 40, 781, 216))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(34)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.PrimaryPushButton = PrimaryPushButton(self.verticalLayoutWidget)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.gridLayout.addWidget(self.PrimaryPushButton, 2, 2, 1, 1)
        self.LineEdit_4 = LineEdit(self.verticalLayoutWidget)
        self.LineEdit_4.setObjectName("LineEdit_4")
        self.gridLayout.addWidget(self.LineEdit_4, 1, 4, 1, 1)
        self.LineEdit_2 = LineEdit(self.verticalLayoutWidget)
        self.LineEdit_2.setObjectName("LineEdit_2")
        self.gridLayout.addWidget(self.LineEdit_2, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 4, 1, 1)
        self.LineEdit = LineEdit(self.verticalLayoutWidget)
        self.LineEdit.setObjectName("LineEdit")
        self.gridLayout.addWidget(self.LineEdit, 1, 0, 1, 1)
        self.LineEdit_5 = LineEdit(self.verticalLayoutWidget)
        self.LineEdit_5.setObjectName("LineEdit_5")
        self.gridLayout.addWidget(self.LineEdit_5, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)
        self.LineEdit_3 = LineEdit(self.verticalLayoutWidget)
        self.LineEdit_3.setObjectName("LineEdit_3")
        self.gridLayout.addWidget(self.LineEdit_3, 1, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setRowStretch(0, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.setStretch(1, 1)
        self.NavigationInterface = NavigationInterface(Form)
        self.NavigationInterface.setGeometry(QtCore.QRect(60, 30, 48, 591))
        self.NavigationInterface.setObjectName("NavigationInterface")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_6.setText(_translate("Form", "数据库设置"))
        self.label_2.setText(_translate("Form", "port"))
        self.PrimaryPushButton.setText(_translate("Form", "确认"))
        self.label.setText(_translate("Form", "数据库url"))
        self.label_9.setText(_translate("Form", "数据库名称"))
        self.label_7.setText(_translate("Form", "用户名"))
        self.label_8.setText(_translate("Form", "密码"))
from qfluentwidgets import LineEdit, NavigationInterface, PrimaryPushButton