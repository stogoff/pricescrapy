# -*- coding: utf-8 -*-
import scrapy
#import sys
#from scrapy.utils.response import open_in_browser

class TescomaShopSpider(scrapy.Spider):
    name = 'tescoma-shop'
    allowed_domains = ['tescoma-shop.ru']
    start_urls = ['http://tescoma-shop.ru/']

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://tescoma-shop.ru/search.asp'

                data = {
                    'search': '1',
                    'phrase': art,
                    'x': '21',
                    'y': '10'

                }
                yield scrapy.http.FormRequest(url=url,
                                              meta={'art': art, 'brand': brand},
                                              formdata=data, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        #open_in_browser(response)
        #sys.exit()
        for table in response.css('table.tb-cat'):
            if art in table.css('td.td-cat-art::text').get():
                title = table.css('td.td-cat-link').css('a::text').get()
                link = table.css('td.td-cat-link').css('a').xpath('@href').get()
                shop = self.name
                price = table.css('span.price::text').getall()[-1].strip()
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
