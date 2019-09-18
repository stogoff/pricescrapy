# -*- coding: utf-8 -*-
import scrapy
import re


class MirposudySpider(scrapy.Spider):
    name = 'mirposudy'
    allowed_domains = ['mirposudy.ru']
    #start_urls = ['http://mirposudy.ru/']

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://mirposudy.ru/catalog/all/?search={}'.format(art)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        for div in response.css('div.offerCard'):
            if art in div.css('div.offerCard__art::text').get():
                title = div.css('div.offerCard__name::text').get()
                price = div.css('div.offerCard__price::text').get()
                price = re.sub(r'\s+', '', price)

                price = re.match(r'\d+', price).group(0)
                link = 'http://mirposudy.ru' + div.css('a.offerCard__wrap').xpath('@href').get()
                shop = self.name

                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
