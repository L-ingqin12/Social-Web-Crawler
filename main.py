

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# 知乎user信息
# https://www.zhihu.com/api/v4/members/chen-xin-36-32-62?include=follower_count,voteup_count,favorited_count,thanked_count%27

# https://zhuanlan.zhihu.com/p/87029765

# https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/quick-start.html

# https://www.zhihu.com/api/v3/explore/guest/feeds?limit=100

# https://api.zhihu.com/people/eed5d99dfd8d987f2346852460ba8071

# https://www.zhihu.com/billboard
# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.common.config import cfg
from app.view.main_window import MainWindow
# from test_main_window import MainWindow

# enable dpi scale
if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# internationalization
locale = cfg.get(cfg.language).value
translator = FluentTranslator(locale)
galleryTranslator = QTranslator()
galleryTranslator.load(locale, "gallery", ".", ":/gallery/i18n")

app.installTranslator(translator)
app.installTranslator(galleryTranslator)

# create main window
w = MainWindow()
w.show()

app.exec_()