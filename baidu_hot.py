import requests
import re
import time
import hashlib
from bs4 import BeautifulSoup


heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
url = 'http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b342_c513'


def sniff_url():
    response = requests.get(url, headers=heads)
    soup = BeautifulSoup(response.content, 'lxml')

    temp_list = []
    for i,index in enumerate(soup.find_all(class_='last')):
        if i > 1:
            temp_list.append(int(index.text))

    item_dict = {}
    for i,title in enumerate(soup.find_all(class_='list-title')):
        key = title.text
        value = temp_list[i]
        item_dict[key] = value

    result = sorted(item_dict.items(), key=lambda d: d[1], reverse=True)
    for item in result:
        print item[0],item[1]





if __name__ == '__main__':
    sniff_url()