# -*- coding: utf-8 -*-
import scrapy
import re
import sys

class AutocoffeeSpider(scrapy.Spider):
    name = 'autocoffee'
    allowed_domains = ['autocoffee.ru']
    start_urls = ['https://autocoffee.ru']
    search = 'https://autocoffee.ru/search/?txt=+{}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                print(art)
                url = self.search.format(brand, art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        shop = self.name
        try:
            div = response.css('div.show_catalog_item')[0]
            title = ' '.join(div.css('div.show_catalog_item_text').css('a').css('span::text').getall())

            title += ' ' + ' '.join(div.css('div.show_catalog_item_text').css('a::text').getall())

            if art in title:
                link = div.css('div.show_catalog_item_text').css('a::attr(href)').get()
                price = div.css('span.priceBlack::text').get()
                price = re.sub(r',|\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
        except IndexError:
            pass
