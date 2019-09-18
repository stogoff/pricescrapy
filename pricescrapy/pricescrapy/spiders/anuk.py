# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.utils.response import open_in_browser


class AnukSpider(scrapy.Spider):
    name = 'anuk'
    allowed_domains = ['anuk-anuk.com']
    start_urls = ['http://anuk-anuk.com/auth/']

    def parse(self, response):
        form_data = {"AUTH_FORM": "Y",
                     "TYPE": "AUTH",
                     "backurl": "/catalog/",
                     "USER_LOGIN": "Prof",
                     "USER_PASSWORD": "proftorg24",
                     "USER_REMEMBER": "Y",
                     "Login": "%C2%EE%E9%F2%E8"
                     }
        return scrapy.FormRequest.from_response(
            response,
            formdata=form_data,
            callback=self.after_login
        )

    def after_login(self, response):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '')
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)



                url = "http://anuk-anuk.com/search/index.php?q={}&s=%CF%EE%E8%F1%EA".format(art)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse_search)

    def parse_search(self, response):
        art = response.meta['art']
        for ar in response.css('div.search-item'):
            link = 'http://anuk-anuk.com' + ar.css('a').xpath('@href').get()
            yield scrapy.Request(url=link, meta={'art': art, 'link': link}, callback=self.parse_item)

    def parse_item(self, response):
        art = response.meta['art']
        link = response.meta['link']
        found_art = ''
        for divtext in response.css('div.catalog-properties::text').getall():
            if divtext[:7] == 'Артикул':
                found_art = divtext[9:]
        if found_art == art:
            title = response.css('h1::text').get().strip()
            price = response.css('div.item-current-price').css('b::text').get()
            price = re.sub(r'\s+', '', price)
            price = re.match(r'\d+', price).group(0)
            shop = self.name
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': shop,
                   'art': art
                   }
