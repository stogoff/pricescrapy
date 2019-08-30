# -*- coding: utf-8 -*-
import scrapy
import re

class AccessoriesforhomeSpider(scrapy.Spider):
    name = 'accessoriesforhome'
    allowed_domains = ['accessoriesforhome.ru']
    start_urls = ['http://accessoriesforhome.ru/']
    search = 'https://accessoriesforhome.ru/search/?module=search&searchword={}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')

                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = self.search.format(art)
                yield scrapy.Request(url=url, meta={'art': art, 'brand': brand}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        for div in response.css('div.item-info'):
            title = div.css('a::text').get()
            if brand.lower() in title.lower():
                link = div.css('a').xpath('@href').get().strip()
                shop = self.name
                price = div.css('div.item-info__price__box::text').get().strip()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }