import re
from pdlearn import mydriver
import sys


# 控制台输入钉钉账号密码
def get_dd():
    """
    通过控制台输入钉钉账号密码
    :return:

    """
    while True:
        dd_name = input('请输入正确的学习强国帐号(钉钉手机号)：')
        ret = re.match(r"^1[3-9]\d{9}$", dd_name)
        if ret:
            pwd = input("请输入学习强国密码：")
            break
    return dd_name, pwd


# 判断当前用户是否存在，不存在保存一条记录
def dd_login_status(username, has_dd=False):
    """
    判断当前用户是否存在,不存在就保存一条新的记录
    :param username: 标识记录名
    :param has_dd: 是否有钉钉账号
    :return:
    """
    while True:
        if has_dd:
            dd_name, pwd = load_dingding("./user/{}/dingding".format(username))
            print("读取用户信息成功")
        else:
            dd_name, pwd = get_dd()
        driver_login = mydriver.Mydriver(no_img=False)
        login_status = driver_login.dd_login(dd_name, pwd)
        if login_status:
            save_dingding("./user/{}/dingding".format(username), dd_name, pwd)
            cookies = driver_login.get_cookies()
            break
    return cookies


# 保存钉钉账户
def save_dingding(user_path, dd_name, pwd):
    """
    保存钉钉账号信息
    :param user_path: 保存信息的路径
    :param dd_name: 账号名字
    :param pwd: 密码
    :return:
    """
    with open(user_path, "w", encoding="utf8") as fp:
        fp.write(dd_name + "," + pwd)


# 加载钉钉账号实现自动登陆
def load_dingding(user_path):
    """
    钉钉账户信息
    :param user_path:
    :type user_path:
    :return:
    :rtype:
    """
    with open(user_path, "r", encoding="utf8") as fp:
        try:
            dd_name, pwd = fp.read().split(",")
            return dd_name, pwd
        except EOFError:
            print("钉钉记录文件损坏，错误代码3程序退出")
            sys.exit(3)
