import re
from pdlearn import mydriver
import sys

'''控制台输入钉钉账号密码'''


def get_dd():
    """
    通过控制台输入钉钉账号密码
    :return:

    """
    while True:
        dname = input('请输入正确的学习强国帐号(钉钉手机号)：')
        ret = re.match(r"^1[3-9]\d{9}$", dname)
        if ret:
            pwd = input("请输入学习强国密码：")
            break
    return dname, pwd


'''判断当前用户是否存在，不存在保存一条记录'''


def dd_login_status(uname, has_dd=False):

    """
    判断当前用户是否存在,不存在就保存一条新的记录
    :param uname: 标识记录名
    :param has_dd: 是否有钉钉账号
    :return:
    """
    while True:
        if has_dd:
            dname, pwd = load_dingding("./user/{}/dingding".format(uname))
            print("读取用户信息成功")
        else:
            dname, pwd = get_dd()
        driver_login = mydriver.Mydriver(noimg=False)
        login_status = driver_login.dd_login(dname, pwd)
        if login_status:
            save_dingding("./user/{}/dingding".format(uname), dname, pwd)
            cookies = driver_login.get_cookies()
            break
    return cookies


'''保存钉钉账号'''


def save_dingding(user_path, dname, pwd):
    """
    保存钉钉账号信息
    :param user_path: 保存信息的路径
    :param dname: 账号名字
    :param pwd: 密码
    :return:
    """
    with open(user_path, "w", encoding="utf8") as fp:
        fp.write(dname + "," + pwd)


'''加载钉钉账号实现自动登陆'''


def load_dingding(user_path):
    """
    加载钉钉账户信息
    :param user_path: 保存信息的路径
    :return:
    """
    with open(user_path, "r", encoding="utf8") as fp:
        try:
            dname, pwd = fp.read().split(",")
            return dname, pwd
        except:
            print("钉钉记录文件损坏，错误代码3程序退出")
            sys.exit(3)
