# -*- coding: utf-8 -*-
import scrapy
import re


class CoffeemanichSpider(scrapy.Spider):
    name = 'coffeemanich'
    allowed_domains = ['coffeemanich.ru']
    start_urls = ['http://coffeemanich.ru/']
    search = "https://www.coffeemanich.ru/search/?q={}&s=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                # grams to kg
                wtre = re.search(r'(\d+)\s*(гр*)', title)
                if wtre:
                    grams = wtre.group(1)
                    word = wtre.group(2)
                    kg = str(int(grams) * 0.001)
                title = re.sub(grams + '\s*' + word, kg + ' кг', title)

                titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(titleplus)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        for link in response.css('div.search-item').css('h4').css('a::attr(href)').getall():
            yield scrapy.Request(url='https://www.coffeemanich.ru' + link,
                             meta={'art': art, 'brand': brand, 'title': tit},
                             callback=self.parse_item)

    def parse_item(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        shop = self.name
        link = response.url
        for div in response.css('div.page-top-main'):
            title = div.css('h1::text').get().strip()

            price = response.css('span.price_value::text').get()
            price = re.sub(r',|\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
