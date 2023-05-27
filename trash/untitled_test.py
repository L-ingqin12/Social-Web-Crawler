import sys

from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
from qfluentwidgets import setThemeColor
from untitled1 import Ui_MainWindow


class main_window(AcrylicWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        setThemeColor('#28afe9')

        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()

        # self.backgroud.setScaledContents(False)
        self.setWindowTitle('Social-Web-Scrapping')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId())
        self.setStyleSheet("main_window{background: rgba(242, 242, 242, 0.8)}")
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)




if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Internationalization
    translator = QTranslator()
    translator.load(QLocale.system(), ":/i18n/qfluentwidgets_")
    app.installTranslator(translator)

    w = main_window()
    w.show()
    app.exec_()