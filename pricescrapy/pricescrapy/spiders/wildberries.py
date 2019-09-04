# -*- coding: utf-8 -*-
import scrapy
import re

class WildberriesSpider(scrapy.Spider):
    name = 'wildberries'
    allowed_domains = ['wildberries.ru']
    start_urls = ['https://wildberries.ru/']

    search = 'https://www.wildberries.ru/catalog/0/search.aspx?search={}%20{}&pagesize=100&sort=popular'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')

                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = self.search.format(brand, title)
                print(url)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title':title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        for div in response.css('div.j-card-item'):
            title = div.css('span.goods-name::text').get()
            words = re.split(r'\s+', title.lower())
            score = 0
            if brand.lower() in words:
                score += 1
            for w in re.split(r'\s+', tit.lower()):
                if w in words:
                    score += 1
            s = score / len(words)
            if s > 0.5:
                link = div.css('a.ref_goods_n_p').xpath('@href').get()
                shop = self.name
                price = div.css('ins.lower-price::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
