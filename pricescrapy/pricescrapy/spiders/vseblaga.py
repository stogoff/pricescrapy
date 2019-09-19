# -*- coding: utf-8 -*-
import scrapy
import re


class VseblagaSpider(scrapy.Spider):
    name = 'vseblaga'
    allowed_domains = ['vseblaga.ru']
    start_urls = ['http://vseblaga.ru/']

    search = 'http://www.vseblaga.ru/partner/search/2/?query={}+{}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')
                title = line.strip().split(';')[2].replace('"','')
                print(art)
                url = self.search.format(brand,art, title)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title':title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        div = response.css('div.product-small')[0]
        title = div.css('h3').css('a').xpath('@title').get()
        words = re.split(r'\s+', title.lower())
        score = 0
        if brand.lower() in words:
            score += 1
        for w in re.split(r'\s+', tit.lower()):
            if w in words:
                score += 1
        s = score / len(words)
        if s > 0.49:
            link = 'http://www.vseblaga.ru' + div.css('h3').css('a').xpath('@href').get()
            shop = self.name
            prices = div.css('span::text').getall()
            if len(prices) > 2:
                price = prices[2]
            elif len(prices) ==1:
                price = prices[0]
            else:
                price = '0'
            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }

