#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019-08-02 16:45 
# @Author : YXH
# @Site :  
# @File : send_email.py 
# @Software: PyCharm


# 发送带有附件的邮件。


import smtplib

from email.mime.text import MIMEText

from email.mime.image import MIMEImage

from email.mime.multipart import MIMEMultipart, MIMEBase

from email import encoders

HOST = "smtp.qq.com"

PORT = "465"

SUBJECT = "测试邮件"

FROM = "123456789@qq.com"

TO = "123456789@qq.com"

# 1> 创建用于发送带有附件文件的邮件对象

# related: 邮件内容的格式，采用内嵌的形式进行展示。

message = MIMEMultipart('related')

# 向message对象中添加不同类型的邮件内容。


# 发送内容是html的邮件，邮件中含有图片。

# 参数2：指定邮件内容类型，默认是plain，表示没有任何格式的纯文本内容。

message_html = MIMEText('<h1>含有图片的邮件：</h1><p>接下来就会展示这个图片了</p><img src="cid:images">', 'html', 'utf8')

# 2> 需要将message_html对象，添加至message中，等待被发送。

message.attach(message_html)


def load_image(path, cid):
    data = open(path, 'rb')

    message_img = MIMEImage(data.read())

    data.close()

    # 给图片绑定cid，将来根据这个cid的值，找到标签内部对应的img标签。

    message_img.add_header('Content-ID', cid)

    # 返回MIMEImage的对象，将该对象放入message中

    return message_img


# 向img标签中指定图片

message.attach(load_image('scrapy_img.png', 'images'))

# 文档附件、图片附件等。

# 一般如果数据是二进制的数据格式，在指定第二个参数的时候，都使用base64，一种数据传输格式。

message_docx = MIMEText(open('test.docx', 'rb').read(), 'base64', 'utf8')

# message_docx['Content-Disposition'] = 'attachment;filename=test.docx'

message_docx.add_header('content-disposition', 'attachment', filename='mytest.docx')

message.attach(message_docx)

message_docx1 = MIMEText(open('测试.docx', 'rb').read(), 'base64', 'utf8')

# 如果文件名是中文的：

# add_header()能够正常的显示中文（推荐）；

# message_docx1['Content-Disposition']是无法正常显示中文的。


# message_docx1['Content-Disposition'] = 'attachment;filename=测试.docx'

message_docx1.add_header('content-disposition', 'attachment', filename='测试.docx')

message.attach(message_docx1)

message_image = MIMEText(open('scrapy_img.png', 'rb').read(), 'base64', 'utf8')

# message_image['Content-Disposition'] = 'attachment;filename=test.png'

message_image.add_header('content-disposition', 'attachment', filename='mytest.png')

message.attach(message_image)

message['From'] = FROM

message['Subject'] = SUBJECT

message['To'] = TO

client = smtplib.SMTP_SSL()

client.connect(HOST, PORT)

print('result: ', client.login(FROM, '授权码（或密码，不推荐使用密码）'))

print('发送结果：', client.sendmail(from_addr=FROM, to_addrs=[TO], msg=message.as_string()))
