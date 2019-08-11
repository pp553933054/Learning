#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/10 8:06 
# @Author : YXH
# @Site :  
# @File : delete_folder.py 
# @Software: PyCharm

import shutil
import os


def delete_file(file_path):
    """
    删除文件
    :param file_path:文件路径
    :type file_path: str
    :return:
    :rtype:
    """

    check_status = False
    # 检测文件是否存在
    if os.path.exists(file_path):
        # myfile = "/tmp/foo.txt"
        myfile = file_path
        # 若是文件路径删除文件
        if os.path.isfile(myfile):
            os.remove(myfile)
            check_status = True
        elif os.path.isdir(myfile):  # 若是文件夹删除夹
            # Try to remove tree; if failed show an error using try...except on screen
            try:
                shutil.rmtree(myfile)
                check_status = True
            except OSError as e:
                # 输出异常
                check_status = False
                print("Error: %s - %s." % (e.filename, e.strerror))
        else:
            print("Error: %s file not found" % myfile)
            check_status = True
    return check_status
