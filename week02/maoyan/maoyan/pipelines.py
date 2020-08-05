# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from maoyan.mysql import ConnDB
import maoyan.config


class MaoyanPipeline:
    def __init__(self, db_info):
        self.db_info = db_info

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_info=maoyan.config.db_info
        )

    def open_spider(self, spider):
        self.conn = ConnDB(self.db_info)
        self.cur = self.conn.getcur()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # movie_name = item["movie_name"]
        # movie_type = item["movie_type"]
        # release_time = item["release_time"]
        # link = item["link"]
        # output = f'{movie_name},{movie_type},{release_time},{link}\r\n'
        # with open('./movie2.txt', 'a+', encoding='gbk') as article:
        #     article.write(output)
        self.conn.insert('movies_info', item)
        return item
