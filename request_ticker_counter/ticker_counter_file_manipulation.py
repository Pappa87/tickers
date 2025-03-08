import os

def list_subfolders(directory):
    return [f.path for f in os.scandir(directory) if f.is_dir()]


def list_files(directory):
    return [f.path for f in os.scandir(directory) if f.is_file()]


def open_file(path):
    file = open(path, encoding="utf-8")
    text = file.read()
    file.close()
    return text