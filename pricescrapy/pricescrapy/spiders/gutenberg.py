# -*- coding: utf-8 -*-
import scrapy
import re

class GutenbergSpider(scrapy.Spider):
    name = 'gutenberg'
    allowed_domains = ['gutenberg.ru']
    start_urls = ['https://gutenberg.ru']
    search = "https://gutenberg.ru/catalog/?q={}&how=r"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        shop = self.name

        for div in response.css('div.catalog_item_wrapp'):
            title = div.css('div.item-title').css('a').css('span::text').get().strip()
            link = self.start_urls[0] + div.css('div.item-title').css('a::attr(href)').get()
            price = response.css('span.price_value::text').get()
            price = re.sub(r',|\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
