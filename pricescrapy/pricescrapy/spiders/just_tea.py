# -*- coding: utf-8 -*-
import scrapy
import re

class JustTeaSpider(scrapy.Spider):
    name = 'just-tea'
    allowed_domains = ['just-tea.ru']
    start_urls = ['https://just-tea.ru/']
    search = "https://just-tea.ru/index.php?route=product/search&search={}"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace('.00', '').replace(',00', '')

                title = line.strip().split(';')[2]
                # titleplus = '+'.join(title.split(' '))
                print(art)
                url = self.search.format(title)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']

        shop = self.name
        for div in response.css('div.product-thumb'):

            title = div.css('div.caption').css('h4').css('a::text').get().strip()
            link = div.css('div.caption').css('h4').css('a::attr(href)').get()
            price = div.css('div.caption').css('p.price::text').get()
            price = re.sub(r',|\s+', '', price)
            price = re.match(r'\d+\.*\d*', price).group(0)
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
