# -*- coding: utf-8 -*-
import scrapy
import re
import requests


class GuruvkusaSpider(scrapy.Spider):
    name = 'guruvkusa'
    allowed_domains = ['guruvkusa.ru']
    start_urls = ['https://guruvkusa.ru']

    search = 'https://guruvkusa.ru/search?lang=ru&q={}{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')

                title = line.strip().split(';')[2]
                # titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(brand[:3], art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title, 'rec': False},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']

        for div in response.css('div.product-card'):
            title = div.css('a.product-link').xpath('@title').get()

            link = self.start_urls[0] + div.css('a.product-link').xpath('@href').get()
            shop = self.name
            price = div.css('span.price::text').get()

            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            if art in title:
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
            else:
                res = requests.get(link).text
                if art in res:
                    yield {'title': title,
                           'link': link,
                           'price': price,
                           'shop': shop,
                           'art': art
                           }

