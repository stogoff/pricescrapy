# -*- coding: utf-8 -*-
import scrapy
import re


class KofeKofeSpider(scrapy.Spider):
    name = 'kofe-kofe'
    allowed_domains = ['kofe-kofe.ru']
    start_urls = ['https://kofe-kofe.ru']
    search = 'https://kofe-kofe.ru/catalog/?q={}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')

                title = line.strip().split(';')[2]
                print(art)
                url = self.search.format(brand, art)
                yield scrapy.Request(url=url,
                                     meta={'art': art, 'brand': brand, 'title': title},
                                     callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        tit = response.meta['title']
        shop = self.name

        for ar in response.css('article.b-good'):

            title = ar.css('div.b-good_info_title::attr(title)').get()
            if re.search(r'арт.\s+' + art + r'\)', title):
                link = self.start_urls[0] + ar.css('div.b-good_info_title').css('a::attr(href)').get()
                price = ar.css('div.b-good_purchase_bar_price::text').get()
                price = re.sub(r',|\s+', '', price)
                price = re.match(r'\d+\.*\d*', price).group(0)
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
