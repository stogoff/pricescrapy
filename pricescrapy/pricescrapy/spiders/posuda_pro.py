# -*- coding: utf-8 -*-
import scrapy
import re


class PosudaProSpider(scrapy.Spider):
    name = 'posuda-pro'
    allowed_domains = ['posuda-pro.ru']

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                #print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')
                title = line.strip().split(';')[2]
                #query = "{} {}".format(art,title)
                print(art)
                url = 'http://posuda-pro.ru/search/?module=search&searchword={}+{}+{}'.format(brand, art, title)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        for div in response.css('div.shop-item'):
            if art in div.css('div.shop_article').css('span.shop_article_value::text').get():
                title = div.css('a.shop-item-title::text').get()
                price = div.css('div.shop-item-price').css('span.price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+', price).group(0)
                link = div.css('a.shop-item-title').xpath('@href').get()
                shop = 'Посуда PRO'

                yield {'title': title,
                           'link': link,
                           'price': price,
                           'shop': shop,
                           'art': art
                           }
