#coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

user = 'root'
password = 'CHZ_Server_0'
port = '3306'
database_name = 'hot_index'
char = 'utf8'

data_url = 'mysql+pymysql://{user}:{password}@localhost:{port}/{database_name}'.format(**locals())

# 最大连接处
engine = create_engine(data_url,max_overflow=10,connect_args={'charset':'utf8'},echo=False)

Base = declarative_base()

Session = sessionmaker(bind=engine)

from sqlalchemy import Column, Integer, String, BigInteger,Float


class WeiboHot(Base):
    __tablename__ = 'weibo_hot'

    id = Column(BigInteger, primary_key=True)

    # 即时排名
    current_rank = Column(Integer)

    time = Column(BigInteger,index=True)

    init_time = Column(BigInteger,index=True)

    title = Column(String(128))

    title_md5 = Column(String(32))

    # 指数
    index = Column(Integer)

    # 相比上一个周期增长
    increase = Column(Float)


def create_table():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_table()

