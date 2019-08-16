import requests
import re

'''获取文章的地址连接'''


def get_article_links():
    """
    获取文章的地址连接
    :return: links数组
    """
    try:
        # temp="https://www.xuexi.cn/4063dbabf4bad826aeeb5d831ce9624e/data60bd1d03c55149fd0e92da70d074d72b.js"
        article = requests.get(
            "https://www.xuexi.cn/c06bf4acc7eef6ef0a560328938b5771/data9a3668c13f6e303932b5e0e100fc248b.js").content.\
            decode(
            "utf8")
        pattern = r"list\"\:(.+),\"count\"\:"
        links = []
        path_list = eval(re.search(pattern, article).group(1))[:20000]
        path_list.reverse()
        for i in range(len(path_list)):
            links.append(path_list[i]["static_page_url"])
        return links
    except Exception:
        print("=" * 120)
        print("get_article_links获取失败")
        print("=" * 120)
        raise


'''获取音像地址连接'''


def get_video_links():
    """
    获取音像地址连接
    :return: 返回links数组
    """
    try:
        # temp="https://www.xuexi.cn/4063dbabf4bad826aeeb5d831ce9624e/data60bd1d03c55149fd0e92da70d074d72b.js"
        video = requests.get(
            "https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js").content.\
            decode("utf8")
        pattern = r'https://www.xuexi.cn/[^,"]*html'
        link = re.findall(pattern, video, re.I)
        link.reverse()
        return link
    except Exception:
        print("=" * 120)
        print("get_video_links获取失败")
        print("=" * 120)
        raise
