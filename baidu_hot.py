import requests
import re
import time
import hashlib
from bs4 import BeautifulSoup
from baidu_hot_model import Session,BaiduHot


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
    for i,item in enumerate(result):
        title = item[0]
        index = item[1]
        insert_to_DB(title,index,i+1)


def insert_to_DB(title,index,rank):
    try:
        title_md5 = get_md5(title)
        index = int(index)
    except Exception,e:
        print e
    else:
        session = Session()
        regular_hot = session.query(BaiduHot).filter(BaiduHot.title_md5==title_md5).first()

        hot = BaiduHot()
        hot.title = title
        hot.time = int(time.time())
        hot.title_md5 = title_md5
        hot.index = index
        hot.current_rank = rank

        if regular_hot and regular_hot.init_time:
            hot.init_time = regular_hot.init_time
        else:
            hot.init_time = int(time.time())

        if regular_hot and regular_hot.index and regular_hot.index != 0 and hot.index:
            hot.increase = (hot.index-regular_hot.index) / float(regular_hot.index)

        try:
            session.add(hot)
            session.commit()
        except Exception,e:
            print e
        finally:
            session.close()


def get_md5(s):
    s = s.encode('utf8') if isinstance(s, unicode) else s
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()



if __name__ == '__main__':
    sniff_url()