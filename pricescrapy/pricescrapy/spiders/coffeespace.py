# -*- coding: utf-8 -*-
import scrapy
import re

class CoffeespaceSpider(scrapy.Spider):
    name = 'coffeespace'
    allowed_domains = ['coffeespace.ru']
    start_urls = ['https://coffeespace.ru/']
    search = "https://coffeespace.ru/catalog/?q={}+{}&s=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')

                title = line.strip().split(';')[2]
                titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(brand, titleplus)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        shop = self.name

        for div in response.css('div.catalog_item_wrapp'):
            title = div.css('div.item-title').css('a.dark_link').css('span::text').get().strip()
            link = div.css('div.item-title').css('a.dark_link::attr(href)').get()
            price = response.css('span.price_value::text').get()
            price = re.sub(r',|\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
