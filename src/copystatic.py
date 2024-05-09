import os
import shutil


def copy_static_to_public():
    if os.path.exists("../public"):
        shutil.rmtree("../public")
        os.mkdir("../public")
    list_dir = os.listdir("../static")
    for directory in list_dir:
        print(directory)

