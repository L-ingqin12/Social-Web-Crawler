import importlib
import subprocess
import shutil
import os
import sys

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))  # sys._MEIPASS
trash_dir = os.path.join(script_dir, "trash")
if not os.path.exists(trash_dir):
    os.makedirs(trash_dir)
#
# # 拼接工作目录的路径
# databases_file = os.path.join(script_dir, "pyecharts/datasets")
#
# # 检查工作目录是否存在，如果不存在则创建
# if not os.path.exists(databases_file):
#     os.makedirs(databases_file)
#
# # 拼接生成文件目录的路径
# wordcloud_dir = os.path.join(script_dir, "wordcloud")
#
# # 检查生成文件目录是否存在，如果不存在则创建
# if not os.path.exists(wordcloud_dir):
#     os.makedirs(wordcloud_dir)
#
# # 获取临时目录路径
# temp_dir = sys._MEIPASS
#
# # 拼接工作目录的路径
# stopwords_file = os.path.join(temp_dir, "stopwords.txt")
# stopwords_file_rename = os.path.join(temp_dir, "stopwords")
# os.rename(stopwords_file, stopwords_file_rename)
#
# shutil.copy2(stopwords_file_rename, wordcloud_dir)
#
# # 拼接生成文件目录的路径
# city_coordinates_file = os.path.join(temp_dir, "city_coordinates.json")
# countries_regions_db_file = os.path.join(temp_dir, "countries_regions_db.json")
# map_filename_file = os.path.join(temp_dir, "map_filename.json")
# shutil.copy2(city_coordinates_file, databases_file)
# shutil.copy2(map_filename_file, databases_file)
# shutil.copy2(countries_regions_db_file, databases_file)

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
