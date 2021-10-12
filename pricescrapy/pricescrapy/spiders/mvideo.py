import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import sys


class MvideoSpider(scrapy.Spider):
    name = 'mvideo'
    allowed_domains = ['mvideo.ru']
    start_urls = ['http://mvideo.ru/']
    search = "https://www.mvideo.ru/product-list-page?q={}+{}"
    urllist = []
    urllist_len = 0

    def parse(self, response, **kwargs):
        pass

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                try:
                    brand = line.strip().split(';')[0]
                    if brand.lower() == 'frap':
                        continue
                    art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()
                except IndexError:
                    continue
                url = self.search.format(brand, art)
                self.urllist.append([url, art])
        self.logger.info(' Goods for search:{}'.format(len(self.urllist)))
        yield self.next_art()

    def next_art(self):
        time.sleep(2)
        try:
            url, art = self.urllist.pop(0)
        except IndexError:
            self.logger.info(' All done.')
            return None
        self.logger.info(' NEXT ART:{}'.format(art))
        self.logger.info(' remaining {}'.format(len(self.urllist)))
        return SeleniumRequest(url=url,
                               dont_filter=True,
                               headers={'Referer': self.start_urls[0]},
                               meta={'art': art},
                               wait_time=5,
                               screenshot=False,
                               callback=self.parse_search)

    def parse_search(self, response):
        art = response.meta['art']
        driver = response.request.meta['driver']
        for x in range(5):
            actions = ActionChains(driver)
            # actions.send_keys(Keys.SPACE)
            actions.send_keys(Keys.PAGE_UP)
            actions.perform()
            time.sleep(.5)
        html = driver.page_source
        soup = bs(html, "html.parser")
        try:
            link = ""
            for a in soup.select('a.product-title__text'):
                link_tmp = a.get('href')
                title_tmp = a.text.strip()
                if art in title_tmp:
                    title, link = title_tmp, link_tmp

            if not link:
                self.logger.info(' NOT FOUND.')
                yield self.next_art()
                return None
            self.logger.info(' FOUND {}'.format(link))

            yield SeleniumRequest(url=link,
                                  meta={'art': art, 'link': link},
                                  callback=self.parse_item,
                                  dont_filter=True, )
        except:
            self.logger.error(' incorrect html')
            driver.get_screenshot_as_file('err/image{}.png'.format(art))
            #self.urllist.append([response.url, art])
            yield self.next_art()
            return None

    def parse_item(self, response):
        art = response.meta['art']
        link = response.meta['link']
        driver = response.request.meta['driver']
        for x in range(5):
            actions = ActionChains(driver)
            actions.send_keys(Keys.SPACE)
            actions.perform()
            time.sleep(.5)
        html = driver.page_source
        soup = bs(html, "html.parser")
        try:
            title = soup.select_one('div.title-brand > h1').text.strip()
            self.logger.info(' {} {}'.format(art, title))
            if (art.lower() in title.lower()) and (art.lower() + '-' not in title.lower()):
                self.logger.info(' ===========')
                try:
                    price = soup.select_one('p.price__main-value').text.strip().replace('\xa0', '').replace('руб.', '')
                except:
                    price = 0
                    self.logger.error(' price not found: {}'.format(soup.select('mvideoru-product-details-card')))

                yield {'title': title,
                       'link': link,
                       'price': price,
                       'shop': self.name,
                       'art': art
                       }
            else:
                self.logger.info(' !!!!!!!!!!!!!!============')
        except:
            self.logger.error(' ITEM ERROR')
            driver.get_screenshot_as_file('err/image_i{}.png'.format(art))
            yield self.next_art()
            return None
        yield self.next_art()
