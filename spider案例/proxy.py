# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import random

import multiprocessing

proxy_list = []

def process(num):
    url = 'http://www.qiushibaike.com/hot/page/' + str(num)
    spider(url)


def spider(url=None,ip=None):
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    ip = random.choice(proxy_list)
    print ip
    try:
       response = requests.get(url, headers=heads,proxies={'http':ip})
    except Exception,e:
        print 'RequestError:',e
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        success = False
        for content in soup.find_all(class_='content'):
            print content.text.strip()
            success = True
        print url + ' -->' + str(success)
            # print content.text.strip()


def grab_proxy():
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    url = 'http://www.kuaidaili.com/free/inha/1/'
    response = requests.get(url, headers=heads)
    print response.text
    soup = BeautifulSoup(response.text, 'lxml')
    result_list = []
    for ip_tr in soup.find_all('tr'):
        td_list = ip_tr.find_all('td')
        if len(td_list) > 6:
            # if 'HTTP' in td_list[5].text:
            ip = td_list[0].text + ':' + td_list[1].text
            print ip
            result_list.append(ip)
    print len(result_list)
    # return result_list


def ip_avail_check(ip_list):
    print len(ip_list)
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    avail_list = []
    for ip in ip_list:
        try:
           response = requests.get('http://47.74.130.48:8003/', headers=heads,proxies={'http':ip})
        except Exception,e:
            print 'RequestError:',e
        else:
            if 'ip' in response.text:
                avail_list.append(ip)

    return avail_list


if __name__ == '__main__':
    global proxy_list
    proxy_list = grab_proxy()
    # for i in range(1,12):
    #     p = multiprocessing.Process(target=process, args=(i,))
    #     p.start()