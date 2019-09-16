# -*- coding: utf-8 -*-
import scrapy
import re


class CavevoSpider(scrapy.Spider):
    name = 'cavevo'
    allowed_domains = ['cavevo.ru']
    start_urls = ['https://cavevo.ru/']

    search = 'https://cavevo.ru/catalog/?q={}+{}&submit=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8'


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
                                     meta={'art': art, 'brand': brand, 'title': title, 'rec':False},
                                     callback=self.parse)

    def parse(self, response):

        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        items = response.css('div.catalog-item-card')
        for div in items:
            title = div.css('a.item-title').css('span::text').get()
            link = 'https://cavevo.ru' + div.css('a.item-title').xpath('@href').get().strip()
            if art in title:

                shop = self.name
                price = div.css('span.catalog-item-price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
            else:
                yield scrapy.Request(url=link,
                                     headers={'Referer': self.start_urls[0]},
                                     meta={'art': art, 'brand': brand, 'title': title, 'rec':False},
                                     callback=self.parse_item)
        if not items:
            if not response.meta['rec']:
                titleplus = '+'.join(tit.split(' '))

                url = self.search.format(brand, titleplus)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': tit, 'rec':True},
                                     headers={'Referer': self.start_urls[0]},
                                     callback=self.parse)


    def parse_item(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        title = response.meta['title']
        link = response.url
        shop = self.name
        article = ''
        for div in response.css('div.catalog-detail-property'):
            if div.css('div.name::text').get() == 'Код производителя':
                article = div.css('div.val::text').get()
        if art == article:
            price = response.css('span.catalog-detail-item-price-current::text').get()
            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
