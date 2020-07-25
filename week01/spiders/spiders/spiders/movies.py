import scrapy
from scrapy.selector import Selector
from spiders.items import SpidersItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board']

    # def parse(self, response):
    #     pass

    # 当爬虫启动时，引擎会自动调用该方法，且只会调用一次，用于生成初始的请求对象(request).
    def start_requests(self):
        url = 'https://maoyan.com/board'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        print(response.url)
        movies = Selector(response=response).xpath('//div[@class="movie-item-info"]')
        for movie in movies:
            item = SpidersItem()

            link = movie.xpath('./p[@class="name"]/a/@href').get()
            # 拼接成完整的url
            link = f'https://maoyan.com{link}'
            releasetime = movie.xpath('p[@class="releasetime"]/text()').get()
            print('------------')
            print(link)
            print(releasetime)
            print('------------')
            item['link'] = link
            item['releasetime'] = releasetime
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        print(response.url)
        item = response.meta['item']
        movie = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        movie_name = movie.xpath('./h1/text()').get()
        movie_type = '/'.join([text.strip() for text in movie.xpath('./ul/li/a/text()').getall()])
        print('------------')
        print(movie_name)
        print(movie_type)
        print('------------')
        item['movie_name'] = movie_name
        item['movie_type'] = movie_type
        yield item
