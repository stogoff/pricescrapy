# -*- coding: utf-8 -*-
import scrapy
import re

class MugduoSpider(scrapy.Spider):
    name = 'mugduo'
    allowed_domains = ['mugduo.ru']
    start_urls = ['https://mugduo.ru/']
    search = "https://www.mugduo.ru/products?keyword={}+{}"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                titleplus = '+'.join(title.split(' '))
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

        for div in response.css('div.product-item__main'):
            title = div.css('a.product-item__title-link::text').get().strip()
            words = re.split(r'\s+', title.lower())
            score = 0
            if brand.lower() in words:
                score += 1
            for w in re.split(r'\s+', tit.lower()):
                if w in words:
                    score += 1
            s = score / len(words)
            if s > 0.5:
                link = self.start_urls[0] + div.css('a.product-item__title-link::attr(href)').get()
                price = response.css('div.product-item__cost-new::text').get()
                price = re.sub(r',|\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
