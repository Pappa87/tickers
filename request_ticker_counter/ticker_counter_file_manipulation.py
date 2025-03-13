import os
import config

def list_subfolders(directory):
    return [f.path for f in os.scandir(directory) if f.is_dir()]


def list_files(directory):
    return [f.path for f in os.scandir(directory) if f.is_file()]


def open_file(path):
    file = open(path, encoding="utf-8")
    text = file.read()
    file.close()
    return text


def get_folders_of_date(date_str):
    date_str = date_str.replace("-", "_")
    filtered_folders = [f"{config.SAVING_FOLDER}/{folder}" for folder in os.listdir(config.SAVING_FOLDER) if folder.startswith(date_str)]
    return filtered_folders