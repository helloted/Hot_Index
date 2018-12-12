# -*- coding:utf-8 -*-

import requests



user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

def main(word):
    url = 'http://dict.youdao.com/jsonapi?q={word}&doctype=json&keyfrom=mac.main&id=\
    7E97E3544A71DD342ABA7145B67B7A31&vendor=appstore&appVer=2.2.3&client=macdict&jsonversion=2'.format(word=word)
    resp = requests.get(url, headers=headers)
    print resp.content


if __name__ == '__main__':
    main('hello')