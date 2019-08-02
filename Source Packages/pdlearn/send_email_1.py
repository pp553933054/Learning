#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-08-02 17:28 
# @Author : YXH
# @Site :  
# @File : send_email_1.py 
# @Software: PyCharm

# coding:utf-8

import smtplib

from email.mime.text import MIMEText

import time

from email.mime.multipart import MIMEMultipart

from email.header import Header

from email import encoders

from email.mime.base import MIMEBase

from email.utils import parseaddr, formataddr

from email.mime.image import MIMEImage


def SendMail(sender, receivers, cc_mail, mail_pass, content, file, image):
    # 第三方 SMTP 服务

    mail_host = "smtp.qq.com"  # 设置服务器

    # message = MIMEText(content, 'plain', 'utf-8')#正文内容   plain代表纯文本

    # 构造一个MIMEMultipart对象代表邮件本身

    message = MIMEMultipart()

    message.attach(MIMEText(content, 'html', 'utf-8'))  # 正文内容   plain代表纯文本,html代表支持html文本

    message['From'] = sender

    message['To'] = ','.join(receivers)  # 与真正的收件人的邮箱不是一回事

    message['Cc'] = ','.join(cc_mail)

    subject = 'Python自动邮件-%s' % time.ctime()

    message['Subject'] = subject  # 邮件标题

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

    # 将图片显示在正文

    with open(image, 'rb') as f:

        # 图片添加到正文

        msgImage = MIMEImage(f.read())

        # 定义图片ID

    msgImage.add_header('Content-ID', '<image1>')

    message.attach(msgImage)

    try:

        smtpObj = smtplib.SMTP_SSL(mail_host, 465)

        smtpObj.login(sender, mail_pass)

        smtpObj.sendmail(sender, receivers + cc_mail, str(message))  # message.as_string()

        smtpObj.quit()

        print
        u"邮件发送成功"

    except smtplib.SMTPException as e:
        print (e)


if __name__ == "__main__":
    sender = 'XXXXXX@qq.com'  # 用户名与发送方

    receivers = ['YYYYYY@qq.com', 'ZZZZZZ@139.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    cc_mail = ['PPPPPP@qq.com']  # 抄送人

    # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

    mail_pass = "iwbhitiyrhbfiecg"

    content = '''抢到票，速度登录12306付款

            <h1>测试</h1>

            <h2 style="color:red">仅用于测试</h1>

            <a href="http://www.runoob.com/python/python-email.html">菜鸟教程</a><br>

            <p>图片演示：</p>

            <p><img src="cid:image1"></p>

          '''

    file = 'Fx1.txt'

    image = 'language.jpg'

    SendMail(sender, receivers, cc_mail, mail_pass, content, file, image)
