#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/2 19:55
# @Author : YXH
# @Site : ${SITE}
# @File : test_properties.py
from unittest import TestCase
from pdlearn import read_config


# @Software: PyCharm
class TestProperties(TestCase):
    def test_get_properties(self):
        # self.assertEqual(True, False)

        # url = cfg_path + '\\' + filename + '\\cfg.properties'

        config=read_config.Properties("..\config.properties")
        obj=config.get_properties()
        self.assertEqual(obj,{'name':'yxh','address':'tianjin'})


if __name__ == '__main__':
    TestCase.main()
