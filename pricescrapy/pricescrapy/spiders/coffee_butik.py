# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import request


class CoffeeButikSpider(scrapy.Spider):
    name = 'coffee-butik'
    allowed_domains = ['coffee-butik.ru']
    start_urls = ['http://coffee-butik.ru']

    search = "https://www.coffee-butik.ru/search/?q={}{}"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()

                title = line.strip().split(';')[2]
                titleplus = ''
                for w in title.split(' '):
                    titleplus += "+" + request.quote(w.encode('cp1251'))

                print(art)
                url = self.search.format(brand, titleplus)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        try:
            link = self.start_urls[0] + response.css('div.api-item-name')[0].css('a::attr(href)').get()
            yield scrapy.Request(url=link,
                                 meta={'art': art, 'brand': brand, 'title': tit},
                                 callback=self.parse_item)
        except IndexError:

            pass
    def parse_item(self,response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        shop = self.name
        link = response.url

        title = response.css('h1::text').get()
        price = response.css('span.item_price_value::text').get()
        price = re.sub(r',|\s+', '', price)
        price = re.match(r'\d+\.*\d*', price).group(0)
        yield {'title': title,
               'link': link,
               'price': price,
               'shop': shop,
               'art': art
               }
