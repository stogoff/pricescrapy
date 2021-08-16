import scrapy
from scrapy_selenium import SeleniumRequest

class TestproxySpider(scrapy.Spider):
    name = 'testproxy'
    allowed_domains = ['iplocation.net']

    def start_requests(self):
        for url in ['https://www.iplocation.net/',]:
            yield SeleniumRequest(url=url,
                              dont_filter=True,
                              headers={'Referer': self.start_urls[0]},
                              meta={'art': art, 'brand': brand},
                              wait_time=3,
                              screenshot=True,
                              callback=self.parse)

    def parse(self, response):
        pass
