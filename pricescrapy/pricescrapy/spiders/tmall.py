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

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                self.logger.info('{}'.format(art))
                url = self.search.format(brand, art)
                yield SeleniumRequest(url=url,
                                      dont_filter=True,
                                      headers={'Referer': self.start_urls[0]},
                                      meta={'art': art, 'brand': brand},
                                      wait_time=5,
                                      screenshot=False,
                                      callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        try:
            price = response.css('div.price').css('span::text').get().replace('\xa0', '')
            price = re.split(r'\W+', price)[0]
            title = ''.join(response.css('a.product').xpath('.//text()').getall())
            title = title.replace("\n", " ").replace("\t", "").strip()
            link = 'https://aliexpress.ru' + response.css('a.product::attr(href)').get().split('?')[0]
            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': self.name,
                   'art': art
                   }
        except:
            pass
