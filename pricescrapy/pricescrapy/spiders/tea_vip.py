# -*- coding: utf-8 -*-
import scrapy
import re


class TeaVipSpider(scrapy.Spider):
    name = 'tea-vip'
    allowed_domains = ['tea-vip.ru']
    start_urls = ['https://tea-vip.ru/']
    search = "https://tea-vip.ru/?s={}&post_type=product"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')

                title = line.strip().split(';')[2]
                # titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        link = response.url
        shop = self.name
        if art in response.css('span.sku::text').get():
            title = response.css('h1.product_title::text').get().strip()
            price = response.css('span.woocommerce-Price-amount::text').get()
            price = re.sub(r',|\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
