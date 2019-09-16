# -*- coding: utf-8 -*-
import scrapy
import re

class HolodilnikSpider(scrapy.Spider):
    name = 'holodilnik'
    allowed_domains = ['holodilnik.ru']
    start_urls = ['http://holodilnik.ru/']

    search = 'http://www.holodilnik.ru/search/?search={} {}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = self.search.format(brand, art)
                yield scrapy.Request(url=url, meta={'art': art, 'brand': brand}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        for div in response.css('div.product-specification'):
            title = div.css('div.product-name').css('span::text').get()
            if art in title:
                link = 'http://holodilnik.ru' + div.css('div.product-name').css('a').xpath('@href').get().strip()
                shop = self.name
                price = div.css('div.price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
