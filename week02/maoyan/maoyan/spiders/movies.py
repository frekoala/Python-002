import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem
import re
import time


class MoviesSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']

    # start_url = ['https://maoyan.com/board']

    # 当爬虫启动时，引擎会自动调用该方法，且只会调用一次，用于生成初始的请求对象(request).
    def start_requests(self):
        urls = 'https://maoyan.com/board'
        yield scrapy.Request(urls, callback=self.parse, dont_filter=False)

    def parse(self, response):
        print('=====parse:%s' % response.request.headers["User-Agent"])
        print('=====parse:%s' % response.request.meta)
        # print(response.url)
        movies = Selector(response=response).xpath('//div[@class="movie-item-info"]')
        try:
            for i in range(10):
                item = MaoyanItem()
                link = movies[i].xpath('./p[@class="name"]/a/@href').get()
                # 拼接成完整的url
                link = f'https://maoyan.com{link}'
                release_time = movies[i].xpath('p[@class="releasetime"]/text()').get()
                item['link'] = link
                item['release_time'] = re.search(r'[0-9].*', release_time).group()
                yield scrapy.Request(url=link, meta={'items': item}, callback=self.parse2)
        except IndexError as identifier:
            print(f'获取movie-item-info标签信息可能为空:{identifier}')

    def parse2(self, response):
        print('=====parse2:%s' % response.request.headers["User-Agent"])
        print('=====parse2:%s' % response.request.meta)
        # print(response.url)
        try:
            movie_info = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
            movie_name = movie_info.xpath('./h1/text()').get()
            movie_type = '/'.join([text.strip() for text in movie_info.xpath('./ul/li/a/text()').getall()])

            item = response.meta['items']
            item['movie_name'] = movie_name
            item['movie_type'] = movie_type
            item['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(item)
            yield item
        except IndexError as identifier:
            print(f'获取movie-brief-container标签信息可能为空:{identifier}')
