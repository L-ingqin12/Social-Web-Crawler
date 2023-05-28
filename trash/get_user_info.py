from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import LineEdit, PrimaryPushButton

from app.common.style_sheet import StyleSheet


class GetUserInfoByUid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(150)
        self.setupUi()
        StyleSheet.HOME_INTERFACE.apply(self)

    def setupUi(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.user_id = LineEdit(self)
        self.user_id.setText("")
        self.user_id.setObjectName("LineEdit")
        self.user_id.setClearButtonEnabled(True)
        self.horizontalLayout.addWidget(self.user_id)
        self.PrimaryPushButton = PrimaryPushButton(self)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout.addWidget(self.PrimaryPushButton)
        self.horizontalLayout.addItem(spacerItem)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("get_user_info_by_uid", "获取知乎用户信息"))
        self.user_id.setWhatsThis(_translate("get_user_info_by_uid", "userid"))
        self.user_id.setPlaceholderText(_translate("get_user_info_by_uid", "userid"))
        self.PrimaryPushButton.setText(_translate("get_user_info_by_uid", "获取"))
        # self.PrimaryPushButton.clicked.connect()