import scrapy
import re
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

import time
import sys


class TmallSpider(scrapy.Spider):
    name = 'tmall'
    allowed_domains = ['tmall.ru']
    start_urls = ['https://tmall.ru/']
    search = 'https://tmall.ru/wholesale?SearchText={}+{}'
    urllist = []
    urllist_len = 0

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                try:
                    brand = line.strip().split(';')[0]
                    if brand.lower() == 'bad_brand':
                        continue
                    art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()
                except IndexError:
                    continue
                url = self.search.format(brand, art)
                self.urllist.append([url, art])
        self.logger.info('Goods for search:{}'.format(len(self.urllist)))
        yield self.next_art()

    def next_art(self):
        time.sleep(2)
        try:
            url, art = self.urllist.pop(0)
        except IndexError:
            self.logger.info('All done.')
            return None
        self.logger.info('NEXT ART:{}'.format(art))
        self.logger.info('remaining {}'.format(len(self.urllist)))
        return SeleniumRequest(url=url,
                                  dont_filter=True,
                                  headers={'Referer': self.start_urls[0]},
                                  meta={'art': art},
                                  wait_time=5,
                                  screenshot=False,
                                  callback=self.parse_search)

    def parse_search(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        try:
            # price = response.css('div.price').css('span::text').get().replace('\xa0', '')
            # price = re.split(r'\W+', price)[0]
            title = ''.join(response.css('a.product').xpath('.//text()').getall())
            title = title.replace("\n", " ").replace("\t", "").strip()
            link = 'https://aliexpress.ru' + response.css('a.product::attr(href)').get().split('?')[0]
            yield SeleniumRequest(url=link,
                                  dont_filter=True,
                                  headers={'Referer': response.url},
                                  meta={'art': art, 'brand': brand, 'title': title},
                                  wait_time=5,
                                  screenshot=False,
                                  callback=self.parse_item)
        except AttributeError:
            self.logger.info('NOT FOUND{}'.format(art))

    def parse_item(self, response):
        art = response.meta['art']
        title = response.meta['title']
        price = response.css('span.product-price-current::text').get().replace('\xa0', '')
        price = re.split(r'\W+', price)[0]
        yield {'title': title,
               'link': response.url,
               'price': price,
               'shop': self.name,
               'art': art
               }
