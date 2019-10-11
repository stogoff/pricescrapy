# -*- coding: utf-8 -*-
import scrapy
import re


class ZelenyisharSpider(scrapy.Spider):
    name = 'zelenyishar'
    allowed_domains = ['zelenyishar.ru']
    start_urls = ['https://zelenyishar.ru']

    search = 'https://www.zelenyishar.ru/catalog/?q={}+{}'

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

        for ar in response.css('article.single-elem'):
            title = ar.css('h4::text').get().strip()

            if art in title:
                link = self.start_urls[0] + ar.css('a::attr(href)').get().strip()
                shop = self.name
                price = ar.css('div.price').css('div.new').css('span::text').get()
                if not price:
                    price = ar.css('div.price').css('span::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
