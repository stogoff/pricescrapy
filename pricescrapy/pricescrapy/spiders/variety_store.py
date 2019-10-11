# -*- coding: utf-8 -*-
import scrapy
import re


class VarietyStoreSpider(scrapy.Spider):
    name = 'variety-store'
    allowed_domains = ['variety-store.ru']
    start_urls = ['http://variety-store.ru/']

    search = 'https://variety-store.ru/search/{}+{}'

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

        for div in response.css('div.product-box-wrapper'):
            title = div.css('div.name').css('a.js-product-link::text').get().strip()

            if art in title:
                link = div.css('a.js-product-link::attr(href)').get().strip()
                shop = self.name
                price = div.css('span.price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
