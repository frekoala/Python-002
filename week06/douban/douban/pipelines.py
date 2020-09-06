# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


db_info = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '111111',
    'db': 'mytestdb'
}


class DoubanPipeline:
    def process_item(self, item, spider):
        return item
