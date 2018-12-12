import requests
from bs4 import BeautifulSoup
import re

heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}


def request_address(address):
    url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain={address}.com'.format(address=address)
    try:
       response = requests.get(url, headers=heads)
    except Exception,e:
        print 'RequestError:',e
    else:
        pattern = re.compile('<returncode>(.*?)</returncode>[\s\S]*?<key>(.*?)</key>[\s\S]*?<original>(.*?):', re.S)
        items = re.findall(pattern, response.text)
        all_item = items[0]
        if len(all_item) == 3:
            re_code = int(all_item[0])
            add = all_item[1]
            ok_code = int(all_item[2])
            if re_code == 200 and ok_code == 210:
                print add
                with open('ok_address.txt','a') as file:
                    file.write(add+'\n')

def rich(length):
    alphabet = [chr(_) for _ in range(ord('a'), ord('z') + 1)]
    fu = [[], alphabet]
    for i in range(1, length):
        fu.append([c + s for c in alphabet for s in fu[i]])
    return fu

if __name__ == '__main__':
    for array in rich(5):
        for item in array:
            print item
            request_address(item)


