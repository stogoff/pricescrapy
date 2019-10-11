# -*- coding: utf-8 -*-
import json

import scrapy


class TvoydomSpider(scrapy.Spider):
    name = 'tvoydom'
    allowed_domains = ['tvoydom.ru']
    start_urls = ['http://tvoydom.ru/']

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()

                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://tvoydom.ru/search/?q={}+{}'.format(brand, art)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        j = json.loads(response.css('vue-search-page').xpath('@json-data').get())
        try:
            p = j['productsInSections'][0]['products'][0]
            title = p['name']
            if art in title:
                link = p['url']
                shop = self.name
                price = p['price']
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
        except IndexError:
            pass
