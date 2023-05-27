import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from qfluentwidgets import LineEdit,  PushButton
from qframelesswindow import FramelessWindow

class LoginWindow(FramelessWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("登录")
        self.resize(400, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # 用户名输入框
        self.username_label = QLabel("用户名：")
        self.username_edit = LineEdit()
        self.username_edit.setClearButtonEnabled(True)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)

        # 密码输入框
        self.password_label = QLabel("密码：")
        self.password_edit = LineEdit()
        self.password_edit .setClearButtonEnabled(True)
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)

        # 登录按钮
        login_button =  PushButton("登录")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if username == "admin" and password == "123456":
            print("登录成功")
        else:
            print("登录失败")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

