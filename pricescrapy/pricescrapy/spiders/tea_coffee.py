# -*- coding: utf-8 -*-
import scrapy
from urllib import request
import re


class TeaCoffeeSpider(scrapy.Spider):
    name = 'tea-coffee'
    allowed_domains = ['tea-coffee.ru']
    start_urls = ['http://www.tea-coffee.ru']
    search = "http://www.tea-coffee.ru/search.php?w={}{}"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                titleplus = ''
                for w in title.split(' '):
                    titleplus += "+" + request.quote(w.encode('cp1251'))

                print(art)
                url = self.search.format(brand, titleplus)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        shop = self.name

        try:
            item_tr = response.css('table.coff_list').css('tr')[0]
            title = item_tr.css('a.a_it::text').get()
            words = re.split(r'\s+', title.lower())
            score = 0
            if brand.lower() in words:
                score += 1
            for w in re.split(r'\s+', tit.lower()):
                if w in words:
                    score += 1
            s = score / len(words)
            if s > 0.5:
                link = self.start_urls[0] + item_tr.css('a.a_it::attr(href)').get()
                price = item_tr.css('span.prteaiz3::text').get()
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
        except IndexError:

            pass
