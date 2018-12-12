# -*- coding:utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import time
import multiprocessing
import gevent
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()

def grab_proxy_from_xici():
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    url = 'http://www.xicidaili.com/wt/1'
    response = requests.get(url, headers=heads)
    soup = BeautifulSoup(response.text, 'lxml')
    proxy_list = []
    for ip_tr in soup.find_all('tr'):
        td_list = ip_tr.find_all('td')
        if len(td_list) > 6:
            if 'HTTP' in td_list[5].text:
                ip = td_list[1].text + ':' + td_list[2].text
                # print ip
                proxy_list.append(ip)
    return proxy_list


def grab_proxy_from_xici2():
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    url = 'http://www.xicidaili.com/wt/2'
    response = requests.get(url, headers=heads)
    soup = BeautifulSoup(response.text, 'lxml')
    proxy_list = []
    for ip_tr in soup.find_all('tr'):
        td_list = ip_tr.find_all('td')
        if len(td_list) > 6:
            if 'HTTP' in td_list[5].text:
                ip = td_list[1].text + ':' + td_list[2].text
                # print ip
                proxy_list.append(ip)
    return proxy_list


def ip_avail_check(ip):
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    avail_list = []
    # print 'check:ip',ip
    try:
       response = requests.get('http://47.74.130.48:8003/', headers=heads,proxies={'http':ip},timeout=5)
    except Exception,e:
        pass
    else:
        if '{"ip":' in response.text:
            avail_list.append(ip)
            print response.text
            return ip


def spider(url=None,ip=None):
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    try:
       response = requests.get(url, headers=heads,proxies={'http':ip},timeout=5)
    except Exception,e:
        print 'RequestError:',e
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        success = False
        for content in soup.find_all(class_='content'):
            success = True
            # print content.text.strip()
        print url + ' -->' + str(success)


def check_with_gevent(pro_list):
    pool = Pool(20)
    for ip in pro_list:
        pool.add(gevent.spawn(ip_avail_check,ip))
    pool.join()


def check_with_multiprocess(pro_list):
    pool = multiprocessing.Pool(processes=5)
    results = []
    for ip in pro_list:
        results.append(pool.apply_async(ip_avail_check, (ip,)))
    pool.close()
    pool.join()
    avail_list = []
    for res in results:
        if res.get():
            avail_list.append(res.get())

if __name__ == '__main__':
    pro_list = grab_proxy_from_xici()
    check_with_gevent(pro_list)

    print 'get avail_list'

    # newPool = multiprocessing.Pool(processes=5)
    #
    # for index,val in enumerate(avail_list):
    #     url = 'http://www.qiushibaike.com/hot/page/' + str(index+1)
    #     newPool.apply_async(spider,(url,val))
    # newPool.close()
    # newPool.join()

