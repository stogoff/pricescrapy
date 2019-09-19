# -*- coding: utf-8 -*-
import scrapy
import re


class AllrightshopSpider(scrapy.Spider):
    name = 'allrightshop'
    allowed_domains = ['allrightshop.ru']
    start_urls = ['http://allrightshop.ru/']

    search = 'https://allrightshop.ru/catalog/?q={}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                titleplus = '+'.join(title.split(' '))
                # query = "{} {}".format(art,title)
                print(art)
                url = self.search.format(brand, titleplus)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        for div in response.css('div.catalog-item-card'):
            title = div.css('a.item-title').css('span::text').get()
            words = re.split(r'\s+', title.lower())
            score = 0
            if brand.lower() in words:
                score += 1
            for w in re.split(r'\s+', tit.lower()):
                if w in words:
                    score += 1
            s = score/len(words)
            if s>0.5:

                link = 'https://allrightshop.ru' + div.css('a.item-title').xpath('@href').get().strip()
                shop = self.name
                price = div.css('span.catalog-item-price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
