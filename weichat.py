import requests


headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 MicroMessenger/6.3.27 NetType/WIFI Language/zh_CN"}
url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxcb27f70254f4a6a5&redirect_uri=http%3A%2F%2Fm.77toupiao.com%2Fwx%2Fback%3Furi%3D%252Fvote%252Fshow%253Fvid%253D1710251433qr6erg%2526page%253D1%2526from%253Dtimeline%2526isappinstalled%253D0%26domain%3Dm.77toupiao.cn&response_type=code&scope=snsapi_userinfo&state=n7mcegsh4rnfrgrrj3ohtfehv4&connect_redirect=1#wechat_redirect'

# url = 'http://127.0.0.1/'

if __name__ == '__main__':
    resp =  requests.get(url,headers=headers)
    print resp.content
