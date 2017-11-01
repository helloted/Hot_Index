import requests
import re
import time
import hashlib
from hot_model import HotModel,Session


heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
url = 'http://s.weibo.com/top/summary'


def sniff_url():
    response = requests.get(url, headers=heads)
    pattern = re.compile('<tr action[\s\S]*?realtimehot[\s\S]*?>(.*?)<\\\/a>[\s\S]*?<span>(.*?)<[\s\S]*?tr>', re.S)
    items = re.findall(pattern, response.text)

    for i,item in enumerate(items):
        title = item[0].decode("unicode-escape")
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
        regular_hot = session.query(HotModel).filter(HotModel.title_md5==title_md5).first()

        hot = HotModel()
        hot.type = 1
        hot.title = title
        hot.time = int(time.time())
        hot.title_md5 = title_md5
        hot.index = index
        hot.current_rank = rank

        if regular_hot and regular_hot.init_time:
            hot.init_time = regular_hot.init_time
            hot.continued_time = hot.time -hot.init_time
        else:
            hot.init_time = int(time.time())
            hot.continued_time = 0

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