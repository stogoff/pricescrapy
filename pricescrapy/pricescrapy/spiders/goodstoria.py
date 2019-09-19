# -*- coding: utf-8 -*-
import scrapy
import re

class GoodstoriaSpider(scrapy.Spider):
    name = 'goodstoria'
    allowed_domains = ['goodstoria.ru']
    start_urls = ['https://goodstoria.ru/']

    search = 'https://goodstoria.ru/search/?q={}+{}&send=Y&r=Y'

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
        title = response.css('h1::text').get()


        link = response.url
        if art in title:
            shop = self.name
            price = response.css('div.item')[0].css('a.price::text').get()
            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
