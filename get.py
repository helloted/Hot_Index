#encoding=utf-8
from weibo_hot_model import WeiboHot,Session


def get_weibo_info():
    session = Session()
    hot_models = session.query(WeiboHot).filter((WeiboHot.time-WeiboHot.init_time) > 12 * 60 * 60).all()
    temp_dict = {}
    for hot in hot_models:
        continued_time = hot.time - hot.init_time
        if hot.title in temp_dict:
            temp_time = temp_dict[hot.title]
            if temp_time < continued_time:
                temp_dict[hot.title] = temp_time
        else:
            temp_dict[hot.title] = continued_time

    for key in temp_dict:
        print key,temp_dict[key]


if __name__ == '__main__':
    get_weibo_info()