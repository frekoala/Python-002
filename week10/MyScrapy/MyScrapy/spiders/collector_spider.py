import scrapy
from scrapy.selector import Selector
from MyScrapy.items import MyscrapyItem


class CollectorSpider(scrapy.Spider):
    name = 'collector'
    allowed_domains = ['www.smzdm.com']

    def start_requests(self):
        urls = 'https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/'
        yield scrapy.Request(urls, callback=self.parse)

    def parse(self, response):
        print('===parsse:%s' % response.request.headers["User-Agent"])
        print('===parsse:%s' % response.request.meta)
        # print(response.url)
        try:
            telepthone = Selector(response=response).xpath('//div[@class="z-feed-content "]')
            if len(telepthone) > 10:
                for i in range(10):
                    name = telepthone[i].xpath('./h5[@class="feed-block-title"]/a/text()').get()
                    content_link = telepthone[i].xpath('./div/div/a[@class="z-group-data"]/@href').get()
                    content_num = int(telepthone[i].xpath('./div/div/a[@class="z-group-data"]/span/text()').get())
                    item = MyscrapyItem()
                    item["name"] = name
                    # 一页30条评论
                    pageSize = 30
                    totalPage = int((content_num + pageSize - 1) / pageSize)
                    print(totalPage)
                    for j in range(totalPage):
                        _link = content_link.rsplit('/', 1)[0] + '/p%s/' % (j + 1) + content_link.rsplit('/', 1)[1]
                        print('_link:%s' % _link)
                        yield scrapy.Request(url=_link, meta={'items': item}, callback=self.parse2)
        except IndexError as identifier:
            print(f'parse获取标签信息可能为空:{identifier}')
        except Exception as e:
            print(f'parse解析有错误:{e}')


    # 解析评论
    def parse2(self, response):
        print('=====parse2:%s' % response.request.headers["User-Agent"])
        print('=====parse2:%s' % response.request.meta)
        print(response.url)
        try:
            conBox = Selector(response=response).xpath('//div[@class="comment_conBox"]')
            for i in range(len(conBox)):
                author = conBox[i].xpath('./div[@class="comment_avatar_time "]/a/span/text()').get()
                description = conBox[i].xpath('./div[@class="comment_conWrap"]/div/p/span/text()').get()
                datePublished = conBox[i].xpath('./div/div[@class="time"]/meta/@content').get()

                item = response.meta['items']
                item['author'] = author
                item['url'] = response.url
                item['datePublished'] = datePublished
                item['description'] = description
                yield item
        except IndexError as identifier:
            print(f'parse2获取标签信息可能为空:{identifier}')
        except Exception as e:
            print(e)
