#encoding=utf-8
from hot_model import HotModel,Session


def get_weibo_info():
    session = Session()
    hot_models = session.query(HotModel).filter(HotModel.continued_time > 24 * 60 * 60).all()
    temp_dict = {}
    for hot in hot_models:
        if hot.title in temp_dict:
            temp_time = temp_dict[hot.title]
            if temp_time < hot.continued_time:
                temp_dict[hot.title] = temp_time
        else:
            temp_dict[hot.title] = hot.continued_time

    for key in temp_dict:
        print key,temp_dict[key]


if __name__ == '__main__':
    get_weibo_info()