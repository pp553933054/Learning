import time
from sys import argv
import random
from pdlearn import version
from pdlearn import user
# from pdlearn import dingding
from pdlearn import mydriver
from pdlearn import score
from pdlearn import threads
from pdlearn import get_links


def user_flag(dd_status, username):
    """
    用户登录状态
    :param username:
    :type username:
    :param dd_status:
    :type dd_status:
    :return:
    :rtype:
    """
    cookies = ''
    if dd_status:
        # cookies = dingding.dd_login_status(uname, has_dd=True)
        pass
    else:
        # if (input("是否保存钉钉帐户密码，保存后可后免登陆学习(Y/N) ")) not in ["y", "Y"]:
        if True:
            driver_login = mydriver.Mydriver(no_head=False)
            cookies = driver_login.login()
        # else:
        #     cookies = dingding.dd_login_status(uname)
        #     pass
    a_log = user.get_a_log(username)
    v_log = user.get_v_log(username)

    return cookies, a_log, v_log


def get_argv():
    no_head = True
    lock = False
    stime = False
    if len(argv) > 2:
        if argv[2] == "hidden":
            no_head = True
        elif argv[2] == "show":
            no_head = False
    if len(argv) > 3:
        if argv[3] == "single":
            lock = True
        elif argv[3] == "multithread":
            lock = False
    if len(argv) > 4:
        if argv[4].isdigit():
            stime = argv[4]
    return no_head, lock, stime


def show_score(cookies):
    """
    获取当前学习积分
    :param cookies:
    :type cookies:
    :return:
    :rtype:
    """
    total, each = score.get_score(cookies)
    print("当前学习总积分：" + str(total))
    print("阅读文章:{}/6,观看视频:{}/6,登陆:{}/1,文章时长:{}/6,视频时长:{}/6".format(*each))
    return total, each


def article(username, cookies, a_log, each, no_head=True):
    """
    阅读文章
    :param no_head:
    :type no_head:
    :param username: 用户标识
    :type username: str
    :param cookies: cookie
    :param a_log: 阅读文章记录
    :param each: 阅读文章数量
    :return:
    """
    if each[0] < 6 or each[3] < 8:
        driver_article = mydriver.Mydriver(no_head=no_head)
        driver_article.get_url("https://www.xuexi.cn/notFound.html")
        driver_article.set_cookies(cookies)
        links = get_links.get_article_links()
        try_count = 0
        while True:
            if each[0] < 6 and try_count < 10:
                a_num = 6 - each[0]
                for i in range(a_log, a_log + a_num):
                    driver_article.get_url(links[i])
                    time.sleep(random.randint(5, 15))
                    for j in range(120):
                        if random.random() > 0.5:
                            driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(j))
                        print("\r文章学习中，文章剩余{}篇,本篇剩余时间{}秒".format(a_log + a_num - i, 120 - j), end="")
                        time.sleep(1)
                    driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, each = show_score(cookies)
                    if each[0] >= 6:
                        print("检测到文章数量分数已满,退出学习")
                        break
                a_log += a_num
            else:
                with open("./user/{}/a_log".format(username), "w", encoding="utf8") as fp:
                    fp.write(str(a_log))
                break
        try_count = 0
        while True:
            if each[3] < 6 and try_count < 10:
                num_time = 60
                driver_article.get_url(links[a_log - 1])
                time.sleep(random.randint(5, 15))
                remaining = (6 - each[3]) * 4 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_article.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r文章时长学习中，文章总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % 120 == 0 and i != remaining:
                        total, each = show_score(cookies)
                        if each[3] >= 6:
                            print("检测到文章时长分数已满,退出学习")
                            break
                driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, each = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("文章学习完成")
        else:
            print("文章学习出现异常，请检查用户名下a_log文件记录数")
        driver_article.quit()
    else:
        print("文章之前学完了")


def video(username, cookies, v_log, each, no_head=True):
    """
    观看视频
    :param no_head:
    :type no_head:
    :param username: 用户标识
    :type username: str
    :param cookies:cookie
    :param v_log: 视频记录
    :param each: 视频数量
    :return:
    """
    if each[1] < 6 or each[4] < 10:
        driver_video = mydriver.Mydriver(no_head=no_head)
        driver_video.get_url("https://www.xuexi.cn/notFound.html")
        driver_video.set_cookies(cookies)
        links = get_links.get_video_links()
        try_count = 0
        while True:
            if each[1] < 6 and try_count < 10:
                v_num = 6 - each[1]
                for i in range(v_log, v_log + v_num):
                    driver_video.get_url(links[i])
                    time.sleep(random.randint(5, 15))
                    for j in range(180):
                        if random.random() > 0.5:
                            driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                        print("\r视频学习中，视频剩余{}个,本次剩余时间{}秒".format(v_log + v_num - i, 180 - j), end="")
                        time.sleep(1)
                    driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, each = show_score(cookies)
                    if each[1] >= 6:
                        print("检测到视频数量分数已满,退出学习")
                        break
                v_log += v_num
            else:
                with open("./user/{}/v_log".format(username), "w", encoding="utf8") as fp:
                    fp.write(str(v_log))
                break
        try_count = 0
        while True:
            if each[4] < 6 and try_count < 10:
                num_time = 60
                driver_video.get_url(links[v_log - 1])
                time.sleep(random.randint(5, 15))
                remaining = (6 - each[4]) * 3 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_video.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r视频学习中，视频总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % 180 == 0 and i != remaining:
                        total, each = show_score(cookies)
                        if each[4] >= 6:
                            print("检测到视频时长分数已满,退出学习")
                            break
                driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, each = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("视频学习完成")
        else:
            print("视频学习出现异常，请检查用户名下v_log文件记录数")
        driver_video.quit()
    else:
        print("视频之前学完了")


if __name__ == '__main__':
    #  0 读取版本信息
    start_time = time.time()
    #  1 创建用户标记，区分多个用户历史纪录
    self_dd_status, self_username = user.get_user()
    info_thread = threads.MyThread("获取更新信息...", version.up_info)
    info_thread.start()
    self_cookies, self_a_log, self_v_log = user_flag(self_dd_status, self_username)
    self_total, self_each = show_score(self_cookies)

    self_no_head, self_lock, s_time = get_argv()
    article_thread = threads.MyThread("文章学习", article, self_username, self_cookies, self_a_log, self_each,
                                      lock=self_lock)
    video_thread = threads.MyThread("视频学习", video, self_username, self_cookies, self_v_log, self_each, lock=self_lock)
    article_thread.start()
    video_thread.start()
    article_thread.join()
    video_thread.join()
    print("总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
    user.shutdown(s_time)
