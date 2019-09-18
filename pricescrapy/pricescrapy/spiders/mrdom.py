# -*- coding: utf-8 -*-
import scrapy
import re

class MrdomSpider(scrapy.Spider):
    name = 'mrdom'
    allowed_domains = ['mrdom.ru']
    start_urls = ['https://www.mrdom.ru']
    search = 'https://www.mrdom.ru/search?q={}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                # titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title, 'rec': False},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        for div in response.css('div.item_content'):
            title = div.css('div.item_title::text').get()
            link = self.start_urls[0] + div.css('a.reset_link::attr(href)').get().strip()
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
            break
