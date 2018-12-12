# -*- coding:utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

heads = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
url = 'http://www.qiushibaike.com/hot/page/1'

response = requests.get(url,headers=heads)

soup = BeautifulSoup(response.text,'lxml')

for content in soup.find_all(class_='content'):
    print content.text.strip()


# for block in soup.find_all(class_='article block untagged mb15'):
#     # print block
#     # author = block.find(class_='author clearfix')
#     # author_tag = author.find(name='h2')
#     # print author_tag.text
#     #
#     # contentHerf = block.find(class_='contentHerf')
#     content = block.find(class_='content')
#     author = block.find(name='h2')
#     if author:
#         print author.text
#     print content.text