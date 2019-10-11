# -*- coding: utf-8 -*-
import scrapy


class EldoradoSpider(scrapy.Spider):
    name = 'eldorado'
    allowed_domains = ['eldorado.ru']
    start_urls = ['https://eldorado.ru/']

    search = 'https://www.eldorado.ru/search/catalog.php?q={}+{}&category='

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = self.search.format(brand, art)
                yield scrapy.Request(url=url,
                                     headers={'Referer': self.start_urls[0]},
                                     meta={'art': art, 'brand': brand}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        try:
            div = response.css('div.item')[0]
            title = div.css('div.itemTitle').css('a::text').get()
            if art in title:
                link = 'https:' + div.css('div.itemTitle').css('a').xpath('@href').get().strip()
                shop = self.name
                price = div.css('meta[itemprop="price"]').xpath('@content').get()
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': shop,
                       'art': art
                       }
        except IndexError:
            pass
