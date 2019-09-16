# -*- coding: utf-8 -*-
import scrapy


class ProvanceSpider(scrapy.Spider):
    name = 'provance'
    allowed_domains = ['provance.ru']
    start_urls = ['http://provance.ru/']


    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://provance.ru/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q={}&dispatch=products.search'.format(art)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        for div in response.css('div.ty-grid-list__item'):
            title = div.css('div.ty-grid-list__item-name').css('a::text').get()
            if art in title:
                shop = 'provance'
                price = div.css('span.ty-price-num::text').get()

                link = div.css('div.ty-grid-list__item-name').css('a').xpath('@href').get()
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                        }
