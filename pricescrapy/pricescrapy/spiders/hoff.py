# -*- coding: utf-8 -*-
import scrapy


class HoffSpider(scrapy.Spider):
    name = 'hoff'
    allowed_domains = ['hoff.ru']
    start_urls = ['http://hoff.ru/']

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')

                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://hoff.ru/search/?fromSearch=direct&search={}%20{}'.format(brand, art)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        quantity = response.css('time.elem-header__date::text').get()[-7:-6]
        if quantity == '1':
            for div in response.css('div.elem-product'):
                title = div.css('div.elem-product__links')[0].css('a::text').get().strip()
                link = div.css('div.elem-product__links')[0].css('a').xpath('@href').get().strip()
                shop = self.name
                price = div.css('div.price-current::text').get().strip()
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }