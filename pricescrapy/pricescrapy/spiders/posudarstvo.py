# -*- coding: utf-8 -*-
import scrapy
import re

class PosudarstvoSpider(scrapy.Spider):
    name = 'posudarstvo'
    allowed_domains = ['posudarstvo.ru']
    start_urls = ['https://posudarstvo.ru']
    search = 'https://posudarstvo.ru/search/?searchstring={}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                # titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(brand, art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title, 'rec': False},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        for div in response.css('div.onegood'):

            title = div.css('p.goodtext').css('a::text').get()
            if art in title:

                link = self.start_urls[0] + div.css('p.goodtext').css('a::attr(href)').get().strip()
                shop = self.name
                price = div.css('span.new-price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
