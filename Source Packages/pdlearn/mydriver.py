import os
import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pdlearn import user_agent

'''浏览器头设置，根据不同的请求初始化对象'''


class Mydriver:
    """
    :keyword
    """

    def __init__(self, no_img=True, nohead=True):
        """
        初始化driver
        :param no_img:
        :type no_img:
        :param nohead:
        :type nohead:
        """
        try:
            self.options = Options()
            if os.path.exists("./chrome/chrome.exe"):  # win
                self.options.binary_location = "./chrome/chrome.exe"
            elif os.path.exists("/opt/google/chrome/chrome"):  # linux
                self.options.binary_location = "/opt/google/chrome/chrome"
            if no_img:
                self.options.add_argument('blink-settings=imagesEnabled=true')  # 不加载图片, 提升速度
            if nohead:
                self.options.add_argument('--headless')
                self.options.add_argument('--disable-extensions')
                self.options.add_argument('--disable-gpu')
                self.options.add_argument('--no-sandbox')
            self.options.add_argument('--mute-audio')  # 关闭声音
            self.options.add_argument('--window-size=400,500')
            self.options.add_argument('--window-position=800,0')
            self.options.add_argument('--log-level=3')

            self.options.add_argument('--user-agent={}'.format(user_agent.getheaders()))
            self.options.add_experimental_option('excludeSwitches', ['disable-automation'])  # 绕过js检测
            self.webdriver = webdriver
            if os.path.exists("./chrome/chromedriver.exe"):  # win
                self.driver = self.webdriver.Chrome(executable_path="./chrome/chromedriver.exe",
                                                    chrome_options=self.options)

            elif os.path.exists("./chromedriver"):  # linux
                self.driver = self.webdriver.Chrome(executable_path="./chromedriver",
                                                    chrome_options=self.options)
            elif os.path.exists("/usr/lib64/chromium-browser/chromedriver"):  # linux 包安装chromedriver
                self.driver = self.webdriver.Chrome(executable_path="/usr/lib64/chromium-browser/chromedriver",
                                                    chrome_options=self.options)
            elif os.path.exists("/usr/local/bin/chromedriver"):  # linux 包安装chromedriver
                self.driver = self.webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",
                                                    chrome_options=self.options)
            else:
                self.driver = self.webdriver.Chrome(chrome_options=self.options)

        except Exception:
            print("=" * 120)
            print("Mydriver初始化失败")
            print("=" * 120)
            raise

    '''扫描二维码登陆'''

    def login(self):
        """
        通过扫描二维码登录
        :return:
        :rtype:
        """
        print("正在打开二维码登陆界面,请稍后")
        self.driver.get("https://pc.xuexi.cn/points/login.html")
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("redflagbox"))
        except exceptions.TimeoutException:
            print("网络缓慢，请重试")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("header"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("footer"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
            self.driver.execute_script('window.scrollTo(document.body.scrollWidth/2 - 200 , 0)')
        try:
            WebDriverWait(self.driver, 30, 0.2).until(lambda driver: driver.find_element_by_id("ddlogin-iframe"))
        except exceptions.TimeoutException:
            print("当前网络缓慢")
        else:
            time.sleep(5)
            self.driver.get_screenshot_as_file("login.png")
            # time.sleep(5)
        try:
            # if os.path.exists("login.png"):
            #     send_email.temp_send()
            # temp = self.get_cookies()
            WebDriverWait(self.driver, 270).until(EC.title_is(u"我的学习"))
            cookies = self.get_cookies()
            return cookies
        except TimeoutError:
            print("扫描二维码超时")

    '''通过钉钉实现登陆'''

    def dd_login(self, d_name, pwd):
        """
        通过钉钉账号  登录
        :param d_name:
        :type d_name:
        :param pwd:
        :type pwd:
        :return:
        :rtype:
        """
        __login_status = False
        self.driver.get(
            "https://login.dingtalk.com/login/index.htm?"
            "goto=https%3A%2F%2Foapi.dingtalk.com%2Fconnect%2Foauth2%2Fsns_authorize"
            "%3Fappid%3Ddingoankubyrfkttorhpou%26response_type%3Dcode%26scope%3Dsnsapi"
            "_login%26redirect_uri%3Dhttps%3A%2F%2Fpc-api.xuexi.cn%2Fopen%2Fapi%2Fsns%2Fcallback"
        )
        self.driver.find_elements_by_id("mobilePlaceholder")[0].click()
        self.driver.find_element_by_id("mobile").send_keys(d_name)
        self.driver.find_elements_by_id("mobilePlaceholder")[1].click()
        self.driver.find_element_by_id("pwd").send_keys(pwd)
        self.driver.find_element_by_id("loginBtn").click()
        try:
            print("登陆中...")
            WebDriverWait(self.driver, 2, 0.1).until(lambda driver: driver.find_element_by_class_name("modal"))
            print(self.driver.find_element_by_class_name("modal").find_elements_by_tag_name("div")[0].text)
            self.driver.quit()
            __login_status = False
        except exceptions.TimeoutException:
            __login_status = True
        return __login_status

    '''获取cookie'''

    def get_cookies(self):
        """
        获取cookie
        :return:
        :rtype:
        """
        cookies = self.driver.get_cookies()
        return cookies

    '''设置cookies'''

    def set_cookies(self, cookies):
        """
        设置cookie
        :param cookies:
        :type cookies:
        :return:
        :rtype:
        """
        for cookie in cookies:
            for k in cookie:
                if k == 'expiry':
                    t = cookie[k]
                    cookie[k] = int(t)  # 时间戳 秒
            self.driver.add_cookie({k: cookie[k] for k in cookie.keys()})

    def get_url(self, url):
        """
        访问浏览器
        :param url:
        :type url:
        :return:
        :rtype:
        """
        self.driver.get(url)

    def go_js(self, js):
        """
        浏览器执行js命令
        :param js:
        :type js:
        :return:
        :rtype:
        """
        self.driver.execute_script(js)

    def quit(self):
        self.driver.quit()
