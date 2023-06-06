# coding:utf-8
import sys
import os
import importlib
import subprocess

REQUIRED_LIBRARIES = ["requests", "numpy", "qfluentwidgets", "PyQt5", "jieba", "wordcloud", "matplotlib", "pyecharts"]


def check_dependencies():
    missing_libraries = []
    for library in REQUIRED_LIBRARIES:
        try:
            importlib.import_module(library)
        except ImportError:
            missing_libraries.append(library)

    if missing_libraries:
        print(f"Missing dependencies: {', '.join(missing_libraries)}")
        return 1  # 返回非零值表示有缺失的依赖库
    else:
        print("All dependencies are installed")
        return 0  # 返回零值表示所有依赖库已安装


def download_dependencies():
    for library in REQUIRED_LIBRARIES:
        print(f"Installing {library}")
        subprocess.run(['pip', 'install', library])


# 检测依赖库
result = check_dependencies()

if result == 1:
    # 缺失依赖库，自动下载
    download_dependencies()
else:
    # 所有依赖库已安装，继续执行程序的其他逻辑
    print("Running the main program")

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
# pyinstaller --upx-dir "D:\Document\Desktop\graduation design\SocialWebScrapping\venv\Scripts" -w -i logo.png demo.py --clean
