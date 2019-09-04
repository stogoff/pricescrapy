# -*- coding: utf-8 -*-
import scrapy
import re

class FgBuySpider(scrapy.Spider):
    name = 'fg-buy'
    allowed_domains = ['fg-buy.ru']
    start_urls = ['http://fg-buy.ru/']

    search = 'https://fg-buy.ru/search/?search={}%20{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')

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
        for div in response.css('div.list-right'):

            title = div.css('a::text').get()
            link = div.css('a').xpath('@href').get().strip()
            if art in title:

                shop = self.name
                price = div.css('span.price-new::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
