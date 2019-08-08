# -*- coding: utf-8 -*-
# @Time : 2019/8/2 19:46
# @Author : YXH
# @Site :
# @File : read_config.py
# @Software: PyCharm
# 读取Properties 文件类


# class Properties(object):
#     """
#     读取配置文件
#     """
#
#     def __init__(self, file_name):
#         """
#         初始化函数
#         :param file_name: 配置文件
#         :type file_name: str
#         """
#
#         self.fileName = file_name
#         self.properties = {}
#
#     def __get_dict(self, str_name, dict_name, value):
#         if str_name.find('.') > 0:
#             k = str_name.split('.')[0]
#             dict_name.setdefault(k, {})
#             return self.__get_dict(str_name[len(k) + 1], dict_name[k], value)
#         else:
#             dict_name[str_name] = value
#             return
#
#     def get_properties(self):
#         """
#         将从配置文件中读取到的属性，以字典的形式返回
#         :return: properties
#         :rtype: dict
#         """
#         try:
#             pro_file = open(self.fileName, 'r', encoding='utf-8')
#             for line in pro_file.readlines():
#                 if line.find('=') > 0:
#                     # stirs = line.replace('\n', '').split('=')
#                     # properties[stirs[0]] = stirs[1]
#                     strs = line.replace('\n', '').split('=')
#                     strs[1] = line[len(strs[0]) + 1:]
#                     self.__get_dict(strs[0].strip(), self.properties, strs[1].strip())
#
#         except Exception as e:
#             raise e
#         else:
#             pro_file.close()
#         return self.properties


class Properties(object):
    """
    配置文件类
    """

    def __init__(self, file_name):
        self.fileName = file_name
        self.properties = {}

    def __get_dict(self, str_name, dict_name, value):

        if str_name.find('.') > 0:
            k = str_name.split('.')[0]
            dict_name.setdefault(k, {})
            return self.__get_dict(str_name[len(k) + 1:], dict_name[k], value)
        else:
            dict_name[str_name] = value
            return

    def get_properties(self):
        """
        读取配置文件
        :return:properties
        :rtype:dict
        """
        try:
            pro_file = open(self.fileName, 'Ur')
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#") != -1:
                    line = line[0:line.find('#')]
                if line.find('=') > 0:
                    parameter = line.split('=')
                    parameter[1] = line[len(parameter[0]) + 1:]
                    self.__get_dict(parameter[0].strip(), self.properties, parameter[1].strip())
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return self.properties
