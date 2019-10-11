# -*- coding: utf-8 -*-
import scrapy
import re

class KibetShopSpider(scrapy.Spider):
    name = 'kibet-shop'
    allowed_domains = ['kibet-shop.ru']
    start_urls = ['https://kibet-shop.ru']

    search = 'https://kibet-shop.ru/search/?q={}%20{}&s=%C2%A0'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()

                title = line.strip().split(';')[2]
                # titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(brand, art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title, 'rec': False},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        for div in response.css('div.catalog-item'):

            title = div.css('a.title').xpath('@title').get()
            link = self.start_urls[0] + div.css('a.title').xpath('@href').get().strip()
            shop = self.name
            price = div.css('div.price').css('b::text').get()
            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
