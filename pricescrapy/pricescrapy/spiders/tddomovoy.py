# -*- coding: utf-8 -*-
##### NOT WORKING
import scrapy
import re

class TddomovoySpider(scrapy.Spider):
    name = 'tddomovoy'
    allowed_domains = ['tddomovoy.ru']
    start_urls = ['http://tddomovoy.ru/']

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://tddomovoy.ru/catalog/?q={}+{}&how=r'.format(brand, art)
                yield scrapy.Request(url=url,
                                     headers={'Referer': 'https://tddomovoy.ru/'},
                                     meta={'art': art},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        for div in response.css('div.bx_catalog_item_container'):
            divt = div.css('div.bx_catalog_item_title')
            title = divt.css('a::text').get()
            if art in title:

                link = 'https://tddomovoy.ru' + divt.css('a').xpath('@href').get()
                shop = self.name

                price = div.css('div.new_price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }