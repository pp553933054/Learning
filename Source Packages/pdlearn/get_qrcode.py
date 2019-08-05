#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/3 16:55 
# @Author : YXH
# @Site :  
# @File : get_qrcode.py
# @Software: PyCharm

import os

import qrcode
from PIL import Image
from pyzbar import pyzbar


def make_qr_code(content, save_path=None):
    """
    生成登录二维码
    :param content: 生成二维码文本
    :type content: str
    :param save_path: 生成二维码的保存路径
    :type save_path: str
    :return:
    :rtype:
    """
    qr_code_maker = qrcode.QRCode(version=5,
                                  error_correction=qrcode.constants.ERROR_CORRECT_M,
                                  box_size=8,
                                  border=4,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    img = qr_code_maker.make_image(fill_color="black", back_color="white")
    if save_path:
        img.save(save_path)
    else:
        img.show()  # 中间图不显示


def make_qr_code_with_icon(content, icon_path, save_path=None):
    """
    生成带中间图的二维码
    :param content: 生成二维码所需文本
    :type content: str
    :param icon_path: 中间图图片路径
    :type icon_path: str
    :param save_path: 生成二维码保存路径
    :type save_path: str
    :return:
    :rtype:
    """
    if not os.path.exists(icon_path):
        raise FileExistsError(icon_path)

    # First, generate an usual QR Code imaghttps://oapi.dingtalk.com/connect/qrcommit?showmenu=false&code=45F5BF17-73DF-4131-9FD9-A6CBCA870F67&appid=dingoankubyrfkttorhpou&redirect_uri=https%3A%2F%2Fpc-api.xuexi.cn%2Fopen%2Fapi%2Fsns%2Fcallbacke
    qr_code_maker = qrcode.QRCode(version=5,
                                  error_correction=qrcode.constants.ERROR_CORRECT_H,
                                  box_size=8,
                                  border=4,

                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    qr_code_img = qr_code_maker.make_image(
        fill_color="black", back_color="white").convert('RGBA')

    # Second, load icon image and resize it
    icon_img = Image.open(icon_path)
    code_width, code_height = qr_code_img.size
    icon_img = icon_img.resize(
        (code_width // 4, code_height // 4), Image.ANTIALIAS)

    # Last, add the icon to original QR Code
    qr_code_img.paste(icon_img, (code_width * 3 // 8, code_width * 3 // 8))

    if save_path:
        qr_code_img.save(save_path)  # 保存二维码图片
        qr_code_img.show()  # 显示二维码图片
    else:
        print("save error!")


def decode_qr_code(code_img_path):
    """
    解码二维码
    :param code_img_path: 二维码保存路径
    :type code_img_path: str
    :return:
    :rtype:
    """
    if not os.path.exists(code_img_path):
        raise FileExistsError(code_img_path)

    # Here, set only recognize QR Code and ignore other type of code
    return pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])


if __name__ == "__main__":
    print("============QRcodetest===============")
    print("         1、Make a QRcode            ")
    print("         2、Scan a QRcode            ")
    print("=====================================")
    print("1、请输入编码信息：")
    code_Data = input('>>:').strip()
    code_Data="https://oapi.dingtalk.com/connect/qrcommit?showmenu=false&code=01879BDD-8239-4387-8D12-7A7D19849D2E&appid=dingoankubyrfkttorhpou&redirect_uri=https%3A%2F%2Fpc-api.xuexi.cn%2Fopen%2Fapi%2Fsns%2Fcallback"
    print("正在编码：")
    # ==生成带中心图片的二维码
    make_qr_code_with_icon(code_Data, "phone.jpg", "qrcode.png")  # 内容，center图片，生成二维码图片
    make_qr_code(code_Data,"qrcode_one.png")
    print("图片已保存，名称为：qrcode.png")
    results = decode_qr_code("qrcode1.png")
    print("2、正在解码：")
    if len(results):
        print("解码结果是：")
        print(results[0].data.decode("utf-8"))
    else:
        print("Can not recognize.")
