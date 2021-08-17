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
                if brand.lower == 'frap':
                    continue
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
            for s in response.css('span'):
                if 'data-pc' in s.attrib.keys():
                    if s.attrib['data-pc'] == 'offer_price':
                        price = s.css('span::text').get().replace(' ', '')
                        break
            for a in response.css('a'):
                if 'data-dy' in a.attrib.keys():
                    link = "https://www.eldorado.ru/" + a.attrib['href']
                    title = a.css("::text").get()
            if art not in link:
                return None
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': self.name,
                   'art': art
                   }
        except:
            pass
