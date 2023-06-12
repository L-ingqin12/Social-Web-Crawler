# coding:utf-8
import sys
import os
import app.utils.enviroment_check

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
# TODO: 进度条
# TODO: stack存储
# TODO: 优化提示
# TODO: 优化界面
# TODO: 编写Test
# TODO: 增加代理ip池
# pyinstaller --clean --upx-dir "D:\Document\Desktop\graduation design\SocialWebScrapping\venv\Scripts" -w -i logo.png demo.py
# pyinstaller --upx-dir "D:\Document\Desktop\graduation design\SocialWebScrapping\venv\Scripts" --add-data "app/utils/lib/stopwords.txt;." --add-data "venv/Lib/site-packages/pyecharts/datasets/city_coordinates.json;." --add-data "venv/Lib/site-packages/pyecharts/datasets/countries_regions_db.json;." --add-data "venv/Lib/site-packages/pyecharts/datasets/map_filename.json;." -w -i logo.png --onefile demo.py --clean
