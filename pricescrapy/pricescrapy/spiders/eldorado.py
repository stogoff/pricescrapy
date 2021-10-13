# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class EldoradoSpider(scrapy.Spider):
    name = 'eldorado'
    allowed_domains = ['eldorado.ru']
    start_urls = ['https://eldorado.ru/']

    search = 'https://www.eldorado.ru/search/catalog.php?q={}+{}&category='
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
                               screenshot=True,
                               callback=self.parse_search)

    def parse_search(self, response):
        art = response.meta['art']

        price = None
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
            for s in soup.select('span'):
                if 'data-pc' in s.attrs.keys():
                    if s.attrs['data-pc'] == 'offer_price':
                        price = s.contents[0].replace(' ', '')
                        print('********************', price)
                        break
            if price:
                li = s.parent.parent.parent.parent.parent
                a = li.select('a')[0]
                link = "https://www.eldorado.ru" + a.attrs['href']
                title = a.contents[0].attrs['alt']
                print('********************', link, title)
                if art.lower() not in link.lower():
                    yield self.next_art()
                    return None
                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': self.name,
                       'art': art
                       }
        except:
            print("ERROR")
            pass

        yield self.next_art()
