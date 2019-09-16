# -*- coding: utf-8 -*-
import scrapy
import re

class IcecreamclubSpider(scrapy.Spider):
    name = 'icecreamclub'
    allowed_domains = ['icecreamclub.ru']
    start_urls = ['http://icecreamclub.ru/']

    search = 'https://icecreamclub.ru/search/?q={}+{}&s=%CF%EE%E8%F1%EA'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                #titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(brand, art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        items = response.css('div.search-item')
        for div in items:
            title = ' '.join(div.css('h4').css('a *::text').getall())

            if art in title:
                link = 'https://icecreamclub.ru' + div.css('h4').css('a::attr(href)').get()
                yield scrapy.Request(url=link,
                                     headers={'Referer': self.start_urls[0]},
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse_item)



    def parse_item(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        title = response.meta['title']
        link = response.url
        shop = self.name

        price = response.css('div.product-item-detail-price-current::text').get()
        price = re.sub(r'\s+', '', price)
        price = re.match(r'\d+\.*\d*', price).group(0)
        yield {'title': title,
               'link': link,
               'price': price,
               'shop': shop,
               'art': art
               }

