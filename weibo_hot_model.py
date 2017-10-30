#coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

user = 'root'
password = 'sql$HeF#pass'
port = '3306'
database_name = 'server'
char = 'utf8'

data_url = 'mysql+pymysql://{user}:{password}@localhost:{port}/{database_name}'.format(**locals())

# 最大连接处
engine = create_engine(data_url,max_overflow=10,connect_args={'charset':'utf8'},echo=False)

Base = declarative_base()

Session = sessionmaker(bind=engine)

from sqlalchemy import Column, Integer, String, BigInteger,DateTime


class WeiboHot(Base):
    __tablename__ = 'weibo_hot'

    id = Column(BigInteger, primary_key=True)
    init_time = Column(BigInteger,index=True)
    datetime = Column(DateTime)
