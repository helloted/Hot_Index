#coding=utf-8
import redis
import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()
import multiprocessing
import time,requests
from bs4 import BeautifulSoup

heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}

class GrabProxyIP():

    def __init__(self):
        self.proxy_queue = 'proxy_queue'
        self.redis_center = redis.StrictRedis(host='localhost', port=6379, db=10)


    def start(self):
        # xici_proxy_p = multiprocessing.Process(target=self.grab_from_xici)
        # xici_proxy_p.start()
        #
        # kuaidaili_proxy_p = multiprocessing.Process(target=self.grab_from_kuaidaili)
        # kuaidaili_proxy_p.start()

        check_p = multiprocessing.Process(target=self.check_avail_ip)
        check_p.start()

    def xici_with_page(self,page):
        url = 'http://www.xicidaili.com/wt/' + str(page)
        print 'grab from: ',url
        response = requests.get(url, headers=heads)
        soup = BeautifulSoup(response.text, 'lxml')
        for ip_tr in soup.find_all('tr'):
            td_list = ip_tr.find_all('td')
            if len(td_list) > 6:
                if 'HTTP' in td_list[5].text:
                    ip = td_list[1].text + ':' + td_list[2].text
                    self.redis_center.lpush(self.proxy_queue, ip)

    def grab_from_xici(self):
        while True:
            for i in range(1,6):
                self.xici_with_page(i)
                time.sleep(6)

    def grab_from_kuaidaili(self):
        while True:
            for i in range(1,6):
                self.kuaidaili_with_page(i)
                time.sleep(6)

    def kuaidaili_with_page(self,page):
        url = 'http://www.kuaidaili.com/free/inha/{page}/'.format(page=page)
        print 'grab from: ', url
        response = requests.get(url, headers=heads)
        soup = BeautifulSoup(response.text, 'lxml')
        for ip_tr in soup.find_all('tr'):
            td_list = ip_tr.find_all('td')
            if len(td_list) > 6:
                ip = td_list[0].text + ':' + td_list[1].text
                self.redis_center.lpush(self.proxy_queue, ip)

    def check_avail_ip(self):
        pool = Pool(60)
        while True:
            task = self.redis_center.blpop(self.proxy_queue, 0)[1]
            pool.add(gevent.spawn(self.ip_check,task))

    def ip_check(self,ip):
        heads = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
        avail_list = []
        # print 'check:ip',ip
        try:
            response = requests.get('http://47.74.130.48:8003/', headers=heads, proxies={'http': ip}, timeout=10)
        except Exception, e:
            # print ip,'xxx'
            pass
        else:
            if '{"ip":' in response.text:
                avail_list.append(ip)
                print ip,'√√√'


if __name__ == '__main__':
    grab = GrabProxyIP()
    grab.start()