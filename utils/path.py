#!usr/bin/env python
# coding=utf-8

__author__ = 'yujun huang'

import os
import other_config

def check_path_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_project_path():
    this_file_path = os.path.dirname(__file__)
    project_path = os.path.abspath(this_file_path + '/..')
    return project_path

def get_cache_path():
    """
    项目路径的上一级目录
    :return:
    """
    parent_path=os.path.abspath(os.path.join(get_project_path(),'..'))
    cache_path = os.path.join(parent_path,other_config.CACHE_FOLDER)
    return check_path_exist(cache_path)

def get_upload_path():
    return get_cache_path()

def get_file_store_path(folder):
    path=os.path.join(get_cache_path(),folder)
    return check_path_exist(path)

def get_template_path():
    return os.path.join(get_project_path(),'templates')

def get_temp_path():
    parent_path = os.path.abspath(os.path.join(get_project_path(), '..'))
    temp_path = os.path.join(parent_path, 'temps')
    return check_path_exist(temp_path)

def get_log_path(_file_):
    folder_path = get_file_store_path('fileShare_log')
    file = os.path.basename(_file_)
    log_filname  = file[ 0:file.index('.') ] + '.log'
    return os.path.join(folder_path, log_filname)

def check_repeat_filename(filename_path, num=1):
    if os.path.exists(filename_path):
        dirname = os.path.dirname(filename_path)
        filename = os.path.basename(filename_path)
        name, ext = filename.split('.')
        if name[-2:-1] == '$':
            origin_name = name[:-2]
        else:
            origin_name = name
        filename2 = "{}${}.{}".format(origin_name, num, ext)
        filename_path = check_repeat_filename(
                            os.path.join(dirname, filename2),
                            num=num + 1)
    return filename_path

if __name__ == '__main__':
    p = check_repeat_filename(__file__)