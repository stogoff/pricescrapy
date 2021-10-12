# -*- coding: utf-8 -*-
import scrapy
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from scrapy_selenium import SeleniumRequest


class WildberriesSpider(scrapy.Spider):
    name = 'wildberries'
    allowed_domains = ['wildberries.ru']
    start_urls = ['https://wildberries.ru/']
    custom_settings = {'CONCURRENT_REQUESTS': '1'}
    search = 'https://www.wildberries.ru/catalog/0/search.aspx?xparams=search%3D{0}+{1}&xshard=&sort=popular&search={0}+{1}'
    urllist = []
    urllist_len = 0

    def parse(self, response, **kwargs):
        pass

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                try:
                    brand = line.strip().split(';')[0]
                    if brand.lower() == 'tescoma':
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
                               screenshot=True,
                               callback=self.parse_search)

    def parse_search(self, response):
        art = response.meta['art']
        # with open('image{}.png'.format(art), 'wb') as image_file:
        #    image_file.write(response.meta['screenshot'])
        driver = response.request.meta['driver']
        for x in range(5):
            actions = ActionChains(driver)
            # actions.send_keys(Keys.SPACE)
            actions.send_keys(Keys.PAGE_UP)
            actions.perform()
            time.sleep(.5)
        html = driver.page_source
        driver.get_screenshot_as_file('scr/image{}.png'.format(art))
        soup = bs(html, "html.parser")
        try:
            notfound_hidden = 'hide' in soup.select('p.searching-results__text')[0].parent.get('class')
            if not notfound_hidden:
                self.logger.info('NOT FOUND.')
                yield self.next_art()
                return None
            r_link = soup.select('a.j-open-full-product-card')[0].get('href').split('?')[0]
            # soup.select('a.j-open-full-product-card.ref_goods_n_p')[0].get('href').split('?')[0]
        except:
            self.logger.error('incorrect html')
            driver.get_screenshot_as_file('err/image{}.png'.format(art))
            # self.urllist.append([response.url, art])
            yield self.next_art()
            raise
            return None
        link = 'https://wildberries.ru' + r_link
        self.logger.info('FOUND LINK: {} {}'.format(art, link))
        yield SeleniumRequest(url=link,
                              meta={'art': art, 'link': link},
                              callback=self.parse_item,
                              dont_filter=True, )

    def parse_item(self, response):
        art = response.meta['art']
        link = response.meta['link']
        try:
            title = response.css('span[data-link="text{:productCard^goodsName}"]::text').get()
            description = response.css('div.j-description').css('p::text').get()
            self.logger.info('{} {}'.format(art, title))
            if (art.lower() in title.lower() + description.lower()) and \
                    (art.lower() + '-' not in title.lower() + description.lower()):
                self.logger.info(' ===========')
                price = response.css('span.price-block__final-price::text').get()
                if not price:
                    price = response.css('span.price-block__commission-current-price::text').get()
                price = price.strip().replace('\xa0', '').replace('₽', '')

                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': self.name,
                       'art': art
                       }
            else:
                self.logger.info('!!!!!!!!!!!!!!============')
        except:
            pass
        yield self.next_art()
