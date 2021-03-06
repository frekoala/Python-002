# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SpidersPipeline:
    def process_item(self, item, spider):
        movie_name = item["movie_name"]
        movie_type = item["movie_type"]
        releasetime = item["releasetime"]
        link = item["link"]
        output = f'{movie_name},{movie_type},{releasetime},{link}\r\n'
        with open('./movie2.txt', 'a+', encoding='gbk') as article:
            article.write(output)
        return item
