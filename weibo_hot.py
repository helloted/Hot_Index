import requests
import re
import time


heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
url = 'http://s.weibo.com/top/summary'


def sniff_url():
    response = requests.get(url, headers=heads)

    # pattern = re.compile('<tr action[\s\S]*?realtimehot[\s\S]*?>(.*?)<\\\/a>[\s\S]*?tr>', re.S)
    pattern = re.compile('<tr action[\s\S]*?realtimehot[\s\S]*?>(.*?)<\\\/a>[\s\S]*?<span>(.*?)<[\s\S]*?tr>', re.S)
    items = re.findall(pattern, response.text)

    for item in items:
        print item[0].decode("unicode-escape"),item[1]
        # print item.decode("unicode-escape")


# def try_pattern():
#     text = '<tr action-type=\\"hover\\">'
#     print text
#     pattern = re.compile('<tr action-type', re.S)
#     items = re.findall(pattern, text)
#     print 'over'
#
#     for item in items:
#         print item

if __name__ == '__main__':
    sniff_url()