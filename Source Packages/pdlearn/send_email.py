#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-08-02 17:28 
# @Author : YXH
# @Site :  
# @File : send_email.py
# @Software: PyCharm

# coding:utf-8

import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pdlearn import read_config


def send_mail(host, sender, receivers, cc_mail, mail_pass, content, file, image):
    """
    发送邮件
    :param host: 第三方 SMTP 服务,设置具体的服务器
    :type host: str
    :param sender: 发送人
    :type sender: str
    :param receivers: 收件人
    :type receivers: list
    :param cc_mail: 抄送人
    :type cc_mail: list
    :param mail_pass: 邮箱授权码
    :type mail_pass: str
    :param content:邮件正文
    :type content:str
    :param file:文本附件
    :type file:str
    :param image:图片
    :type image:str
    :return:
    :rtype:
    """
    # 第三方 SMTP 服务,设置具体的服务器

    mail_host = host

    # 正文内容   plain代表纯文本
    # message = MIMEText(content, 'plain', 'utf-8')

    # 构造一个MIMEMultipart对象代表邮件本身
    message = MIMEMultipart()

    # 正文内容   plain代表纯文本,html代表支持html文本
    message.attach(MIMEText(content, 'html', 'utf-8'))
    # 发送人邮箱
    message['From'] = sender
    # 收件人邮箱
    message['To'] = ','.join(receivers)  # 与真正的收件人的邮箱不是一回事
    # 抄送人邮箱
    message['Cc'] = ','.join(cc_mail)
    # 邮件标题
    subject = 'Python自动邮件-%s' % time.ctime()
    message['Subject'] = subject

    # 添加文件到附件

    with open(file, 'rb') as f:

        # MIMEBase表示附件的对象

        mime = MIMEBase('text', 'txt', filename=file)

        # filename是显示附件名字

        mime.add_header('Content-Disposition', 'attachment', filename=file)

        # 获取附件内容

        mime.set_payload(f.read())

        encoders.encode_base64(mime)

        # 作为附件添加到邮件

        message.attach(mime)

    with open(image, 'rb') as f:

        # 图片添加到附件

        mime = MIMEBase('image', 'image', filename=image)

        mime.add_header('Content-Disposition', 'attachment', filename=image)

        mime.set_payload(f.read())

        encoders.encode_base64(mime)

        message.attach(mime)

    with open(image, 'rb') as f:

        # 图片添加到正文

        msg_image = MIMEImage(f.read())

        # 定义图片ID

        msg_image.add_header('Content-ID', '<image1>')

        message.attach(msg_image)

    try:

        smtp_obj = smtplib.SMTP_SSL(mail_host, 465)

        smtp_obj.login(sender, mail_pass)
        # message.as_string()
        smtp_obj.sendmail(sender, receivers + cc_mail, str(message))

        smtp_obj.quit()

        print(u"邮件发送成功")

    except smtplib.SMTPException as e:
        print(e)


def temp_send():
    # 第三方SMTP服务, 设置具体的服务器
    config = read_config.Properties(r"..\config.properties")
    obj = config.get_properties()
    host = obj.get("host")
    # 用户名与发送方
    sender = obj.get("sender")
    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    receivers = obj.get("receivers")
    # 抄送人
    copy_mail = obj.get("copy_mail")

    # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

    password = obj.get("password")

    this_content = '''获取到二维码，速度登录移动端学习强国进行扫描登陆

            <h1>测试</h1>

            <h2 style="color:red">仅用于测试</h1>

            <a href="http://www.runoob.com/python/python-email.html">菜鸟教程</a><br>

            <p>图片演示：</p>

            <p><img src="cid:image1"></p>

          '''

    this_file = 'Fx1.txt'

    this_image = '../login.png'

    send_mail(host, sender, receivers, copy_mail, password, this_content, this_file, this_image)
