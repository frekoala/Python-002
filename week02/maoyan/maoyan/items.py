# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    movie_name = scrapy.Field()
    movie_type = scrapy.Field()
    release_time = scrapy.Field()
    link = scrapy.Field()
    update_time = scrapy.Field()
