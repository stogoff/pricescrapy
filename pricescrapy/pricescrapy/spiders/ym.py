# -*- coding: utf-8 -*-
import scrapy


class YmSpider(scrapy.Spider):
    name = 'ym'
    allowed_domains = ['market.yandex.ru']

    def start_requests(self):
        queries = ['420866', ]  # ,'630040']
        brand = 'Agness'
        with open('input.txt') as f:
            for line in f.readlines():
                brand = line.strip().split('\t')[0]
                query = line.strip().split('\t')[1]
                print(query)
                url = 'https://market.yandex.ru/search?text={} {}&cvredirect=2&local-offers-first=0'.format(brand,query)
                yield scrapy.Request(url=url, meta={'query': query}, callback=self.parse)


    def parse(self, response):
        query = response.meta['query']
        for div in response.css('div.n-snippet-card2'):
            if query in div.css('div.n-snippet-card2__title').css('a').xpath('@title').get():
                title = div.css('div.n-snippet-card2__title').css('a').xpath('@title').get()
                price = div.css('div.price::text').get()
                link = div.css('div.n-snippet-card2__title').css('a').xpath('@href').get()
                shop = div.css('div.n-snippet-card2__shop-name').css('a::text').get()
                if link[:2] == '/p':
                    link = link.split('?')[0] + '/offers?track=average_price'
                    yield scrapy.Request('https://market.yandex.ru' + link, meta={'query': query},
                                         callback=self.parse_id)
                else:
                    yield {'title': title,
                           'link': 'https:' + link,
                           'price': price,
                           'shop': shop,
                           'query':query
                           }

    def parse_id(self, response):
        query = response.meta['query']
        for div in response.css('div.snippet-card'):
            title = div.css('span.snippet-card__header-text::text').get()
            link = div.css('h3.snippet-card__header').css('a').xpath('@href').get()
            shop = div.css('div.snippet-card__shop').css('img').xpath('@alt').get()
            if shop is None:
                shop = div.css('div.n-snippet-card__shop-primary-info').css('a').xpath('@title').get()
            price = div.css('div.price::text').get()
            yield {'title': title,
                   'link': 'https:' + link,
                   'price': price,
                   'shop': shop,
                   'query':query
                   }
