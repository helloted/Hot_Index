# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import requests

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    resp = requests.get(url,headers=headers)


    print type(resp.content)

    pattern = re.compile('<div.*?author.*?<a.*?<img.*?/>.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?<div.*?content.*?<span>(.*?)</span>.*?</div>.*?</a>', re.S)
    items = re.findall(pattern, resp.content)
    print 'finish'

    for item in items:
        print item[0]
        print item[1]

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason


