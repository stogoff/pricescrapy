# -*- coding: utf-8 -*-
import scrapy
import re


class SoskidkoiSpider(scrapy.Spider):
    name = 'soskidkoi'
    allowed_domains = ['соскидкой.москва']
    start_urls = ['https://соскидкой.москва']
    search = "https://соскидкой.москва/search/?query={}+{}"

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
        for div in response.css('div.product'):

            title = div.css('div.h5').css('a::attr(title)').get()
            article = ''
            for tr in div.css('tr'):
                if tr.css('td.name::text').get() == 'Артикул':
                    article = tr.css('td.value').css('div.listfeatures-values::text').get().strip()
                    break


            if art in article:

                link = self.start_urls[0] + div.css('div.h5').css('a::attr(href)').get()
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
