# -*- coding: utf-8 -*-
import scrapy
import re

class AnukSpider(scrapy.Spider):
    name = 'anuk'
    allowed_domains = ['anuk-anuk.com']
    start_urls = ['http://anuk-anuk.com/']

    def start_requests(self):
        with open('/tmp/uploads/input.txt') as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1]
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = "http://anuk-anuk.com/search/index.php?q={}}&s=%CF%EE%E8%F1%EA".format(art)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        for ar in response.css('div.search-item'):
            link = 'http://anuk-anuk.com/' + ar.css('a').xpath('@href').get()
            yield scrapy.Request(url=link, meta={'art': art, 'link': link}, callback=self.parse_item)

    def parse_item(self, response):
        art = response.meta['art']
        link = response.meta['link']
        found_art = ''
        for div in response.css('div.stocks'):
            if div.css('span.posle::text').get() == 'Артикул':
                found_art = div.css('span.har_value::text').get().strip()
        if found_art == art:
            title = response.css('h1.detail__name::text').get().strip()
            price = response.css('div.price__pdv::text').get()
            price = re.sub(r'\s+', '', price)

            price = re.match(r'\d+', price).group(0)
            shop = 'R посуда'
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
