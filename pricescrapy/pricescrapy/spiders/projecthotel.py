# -*- coding: utf-8 -*-
import scrapy
import re


class ProjecthotelSpider(scrapy.Spider):
    name = 'projecthotel'
    allowed_domains = ['projecthotel.ru']

    def start_requests(self):
        with open('/tmp/uploads/input.txt') as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1]
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://projecthotel.ru/catalog'
                data = {
                    'query': art,

                }
                yield scrapy.http.FormRequest(url=url, meta={'art': art}, formdata=data, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        for div in response.css('div.item'):
            if art in div.css('div.article::text').get():
                title = div.css('div.title::text').get()
                price = div.css('div.price::text').get().strip()
                price = re.sub(r'\,', '', price)
                #price = re.match(r'\d+', price).group(0)
                link = 'https://projecthotel.ru' + div.css('a').xpath('@href').get()
                shop = 'проект 2015'

                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
