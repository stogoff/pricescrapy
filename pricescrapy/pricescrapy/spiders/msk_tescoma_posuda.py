# -*- coding: utf-8 -*-
import scrapy
import re


class MskTescomaPosudaSpider(scrapy.Spider):
    name = 'msk-tescoma-posuda'
    allowed_domains = ['msk.tescoma-posuda.ru']
    start_urls = ['https://msk.tescoma-posuda.ru']

    search = 'http://msk.tescoma-posuda.ru/search/?searchstring={}&x=0&y=0' ## article only!!!

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                # titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format( art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        for products in response.css('div.product_list'):
            for div in products.css('div.one'):
                title = div.css('div.name::text').get().strip()
                sku = div.css('div.sku::text').get()
                if art in sku:
                    link = self.start_urls[0] + div.css('div.title').css('a::attr(href)').get().strip()
                    shop = self.name
                    price = div.css('div.price::text').get()
                    price = re.sub(r'\s+', '', price)
                    price = re.match(r'\d+\.*\d*', price).group(0)
                    yield {'title': title,
                           'link': link,
                           'price': price,
                           'shop': shop,
                           'art': art
                           }
