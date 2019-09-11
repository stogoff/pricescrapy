# -*- coding: utf-8 -*-
import scrapy
import re

class TdgaemSpider(scrapy.Spider):
    name = 'tdgaem'
    allowed_domains = ['tdgaem.ru']
    start_urls = ['http://tdgaem.ru/']

    search = 'https://tdgaem.ru/search?lang=ru&q={}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')
                title = line.strip().split(';')[2].replace('"', '')
                titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(brand,  titleplus)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        tit = re.sub('[^0-9a-zA-Zа-яА-Я]+',' ', tit)
        div = response.css('div.product-card')[0]
        title = div.css('a.product-link').xpath('@title').get()
        t = re.sub('[^0-9a-zA-Zа-яА-Я]+',' ', title)
        words = re.split(r'\s+', t.lower())
        score = 0
        if brand.lower() in words:
            score += 1
        for w in re.split(r'\s+', tit.lower()):
            if w in words:
                score += 1
        s = score / len(words)
        if s > 0.49:
            link = 'http://tdgaem.ru' + div.css('a.product-link').xpath('@href').get()
            shop = self.name
            price = div.css('span.price::text').get()

            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }

