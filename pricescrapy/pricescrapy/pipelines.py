# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, String, Integer

# db settings
#dbuser = 'user' #DB username
#dbpass = 'password' #DB password
#dbhost = 'localhost' #DB host
#dbname = 'scrapyspiders' #DB database name
#engine = create_engine("mysql://%s:%s@%s/%s?charset=utf8&use_unicode=0"
#                       %(dbuser, dbpass, dbhost, dbname),
#                       echo=False,
#                       pool_recycle=1800)

engine = create_engine('sqlite:////tmp/newprices.db')
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))

Base = declarative_base()


class AllData(Base):
    __tablename__ = 'alldata'

    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    link = Column(String(1000))
    price = Column(String(30))
    shop = Column(String(100))
    art = Column(String(50))

    def __init__(self, id=None, title=None, link=None, price=None, shop=None, art=None):
        self.id = id
        self.title = title
        self.link = link
        self.price = price
        self.shop = shop
        self.art = art

    def __repr__(self):
        return "<AllData: id='%d', title='%s', link='%s', price='%s', shop='%s', art='%s'>" % \
               (self.id, self.title, self.link, self.price, self.shop, self.art)



class AddTablePipeline(object):



    def process_item(self, item, spider):
        Base.metadata.create_all(engine)
        # create a new SQL Alchemy object and add to the db session
        record = AllData(title=item['title'],
                         link=item['link'],
                         price=item['price'],
                         shop=item['shop'],
                         art=item['art'])
        db.add(record)
        db.commit()

        with open(spider.settings.get('OUTPUT_FILENAME'),'a') as file:
            file.write("{};{};{};{};{}\n".format(item['art'],item['title'],item['price'],item['shop'],item['link']))
        
        return item


class PricescrapyPipeline(object):
    def process_item(self, item, spider):
        return item


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    record = AllData(title='1',
                     link='link',
                     price='price',
                     shop='shop',
                     art='QQQ')
    db.add(record)
    db.commit()
