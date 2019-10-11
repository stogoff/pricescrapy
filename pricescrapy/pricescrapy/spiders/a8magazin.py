# -*- coding: utf-8 -*-
import scrapy
import re


class A8magazinSpider(scrapy.Spider):
    name = 'a8magazin'
    allowed_domains = ['8magazin.ru']
    start_urls = ['https://8magazin.ru']

    search = "https://8magazin.ru/search/?query={}+{}"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()

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
        ul = response.css('ul.tv_products')[0]
        for li in ul.css('li'):
            title = li.css('span[itemprop="name"]::text').get().strip()

            if art in title:
                link = li.css('div.product_title').css('a::attr(href)').get().strip()
                shop = self.name
                price = li.css('span[itemprop="price"]::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
