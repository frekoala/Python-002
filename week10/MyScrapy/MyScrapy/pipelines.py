# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from MyScrapy.mysql import ConnDB
import MyScrapy.config


class MyscrapyPipeline:
    def __init__(self, db_info):
        self.db_info = db_info

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_info=MyScrapy.config.db_info)

    def open_spider(self, spider):
        self.conn = ConnDB(self.db_info)
        self.cur = self.conn.getcur()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.conn.insert('telephone', item)
        return item
