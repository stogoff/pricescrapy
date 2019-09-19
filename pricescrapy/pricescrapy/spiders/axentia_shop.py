# -*- coding: utf-8 -*-
import scrapy
import re

class AxentiaShopSpider(scrapy.Spider):
    name = 'axentia-shop'
    allowed_domains = ['axentia-shop.ru']
    start_urls = ['http://axentia-shop.ru/']

    search = 'https://axentia-shop.ru/products?keyword={}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')
                title = line.strip().split(';')[2]
                print(art)
                url = self.search.format(brand, art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title':title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        shop = self.name
        try:
            div = response.css('div.catalog-element-right')[0]
            title = div.css('div.catalog-element-name').css('h1::text').get()

            link = response.url

            price = div.css('span.pr::text').get()
            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
        except IndexError: ## Нет в наличии
            try:
                div = response.css('div.catalog-item_inner')[0]
                title = div.css('div.catalog-item-name').css('a::text').get()
                link = 'https://axentia-shop.ru' + div.css('div.catalog-item-name').css('a').xpath('@href').get()
                price = div.css('span.pr::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                           'link': link,
                           'price': price,
                           'shop': shop,
                           'art': art
                           }
            except IndexError:
                pass

