import os
from time import sleep
from pdlearn import input_username


def get_user():
    # if len(argv) > 1:
    #     uname = argv[1]
    # else:
    #     uname = input("输入用户标记名：")

    uname = input_username.read_input()

    if check_username(uname):
        # dd = check_dd(uname)
        dd = False
        pass
    else:
        os.makedirs("./user/{}".format(uname))
        dd = False
    return dd, uname


def check_username(username):
    """
    校验用户是否存在
    :param username:
    :type username:
    :return:
    :rtype:
    """
    __check_status = False
    if os.path.exists("./user/{}".format(username)):
        __check_status = True
    return __check_status


def check_dd(uname):
    """
    校验钉钉账号登陆状态
    :param uname:
    :type uname:
    :return:
    :rtype:
    """
    __dd_status = False
    if os.path.exists("./user/{}/dingding".format(uname)):
        __dd_status = True
    return __dd_status


def get_a_log(uname):
    """
    获取文章记录文件
    :param uname:
    :type uname:
    :return:
    :rtype:
    """
    __a_log = 0
    if os.path.exists("./user/{}/a_log".format(uname)):
        with open("./user/{}/a_log".format(uname), "r", encoding="utf8") as fp:
            __a_log = int(fp.read())
    else:
        with open("./user/{}/a_log".format(uname), "w", encoding="utf8") as fp:
            fp.write(str(__a_log))
    return __a_log


def get_v_log(uname):
    """
    获取视频记录文件
    :param uname:
    :type uname:
    :return:
    :rtype:
    """
    __v_log = 0
    if os.path.exists("./user/{}/v_log".format(uname)):
        with open("./user/{}/v_log".format(uname), "r", encoding="utf8") as fp:
            __v_log = int(fp.read())
    else:
        with open("./user/{}/v_log".format(uname), "w", encoding="utf8") as fp:
            fp.write(str(__v_log))
    return __v_log


def shutdown(stime):
    """
    关闭计算机
    :param stime:
    :type stime:
    :return:
    :rtype:
    """
    if stime:
        stime = int(stime)
        os.system('shutdown -s -t {}'.format(stime))
        for i in range(stime):
            print("\r{}秒后关机".format(stime - i), end="")
            sleep(1)
    else:
        print("无自动关机任务，已释放程序内存，10分钟后窗口将自动关闭")
        sleep(600)
