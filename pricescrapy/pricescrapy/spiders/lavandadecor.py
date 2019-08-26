# -*- coding: utf-8 -*-
import scrapy


class LavandadecorSpider(scrapy.Spider):
    name = 'lavandadecor'
    allowed_domains = ['lavandadecor.ru']
    start_urls = ['http://lavandadecor.ru/']



def start_requests(self):
    with open('/tmp/uploads/input.txt') as f:
        for line in f.readlines():
            # print(line.strip().split(';'))

            brand = line.strip().split(';')[0]
            art = line.strip().split(';')[1]
            title = line.strip().split(';')[2]
            # query = "{} {}".format(art,title)
            print(art)
            url = 'https://lavandadecor.ru/search?q={}}'.format(art)
            yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)


def parse(self, response):
    art = response.meta['art']
    for div in response.css('div.ty-grid-list__item'):
        title = div.css('div.ty-grid-list__item-name').css('a::text').get()
        if art in title:
            shop = 'provance-shop'
            price = div.css('span.ty-price-num::text').get()

            link = div.css('div.ty-grid-list__item-name').css('a').xpath('@href').get()
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
