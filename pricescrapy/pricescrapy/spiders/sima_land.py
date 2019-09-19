# -*- coding: utf-8 -*-
import scrapy
import re

class SimaLandSpider(scrapy.Spider):
    name = 'sima-land'
    allowed_domains = ['sima-land.ru']
    start_urls = ['https://sima-land.ru/']

    search = 'https://www.sima-land.ru/search/?q={}%20{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

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
        div = response.css('div.product__info')[0]
        title = response.css('h1::text').get()
        for li in div.css('li.b-properties__item'):
            if li.css('span.b-properties__label::text').get() == 'Артикул поставщика':
                article = li.css('span.b-properties__value::text').get()

        link = response.url
        if art == article:
            shop = self.name
            price = div.css('span.price__val').css('span::text').get()
            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
