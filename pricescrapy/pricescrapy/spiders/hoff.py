# -*- coding: utf-8 -*-
import scrapy
import re

class HoffSpider(scrapy.Spider):
    name = 'hoff'
    allowed_domains = ['hoff.ru']
    start_urls = ['http://hoff.ru/']

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()

                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://hoff.ru/search/?fromSearch=direct&search={}%20{}'.format(brand, art)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        try:
            quantity = response.css('time.elem-header__date::text').get()[-7:-6]
        except:
            quantity = ''
        if quantity == '1':
            for div in response.css('div.elem-product'):
                title = div.css('div.elem-product__links')[0].css('a::text').get().strip()
                link = 'https://hoff.ru' + div.css('div.elem-product__links')[0].css('a').xpath('@href').get().strip()
                shop = self.name
                price = div.css('div.price-current::text').get().strip()
                price = re.sub(r'\s+', '', price)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
