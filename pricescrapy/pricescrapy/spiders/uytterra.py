# -*- coding: utf-8 -*-
import scrapy
import re

class UytterraSpider(scrapy.Spider):
    name = 'uytterra'
    allowed_domains = ['uytterra.ru']
    start_urls = ['https://uytterra.ru']
    search = 'https://uytterra.ru/search/?query={}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

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
        for li in response.css('li.list-item'):

            title = li.css('div.h5::text').get()
            article = li.css('div.title_padding::text').get()
            if art in article:

                link = self.start_urls[0] + li.css('a.item_link::attr(href)').get().strip()
                shop = self.name
                price = li.css('span.price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
