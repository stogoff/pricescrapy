import scrapy
import time
from scrapy_selenium import SeleniumRequest


class OzonSpider(scrapy.Spider):
    name = 'ozon'
    allowed_domains = ['ozon.ru']
    start_urls = ['http://ozon.ru/']
    search = "https://www.ozon.ru/search/?from_global=true&text={}+{}"

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                time.sleep(2)
                brand = line.strip().split(';')[0].lower()
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)

                url = self.search.format(brand, art)
                self.logger.info('{}  {}'.format(art, url))
                yield SeleniumRequest(url=url,
                                             dont_filter=True,
                                             headers={'Referer': self.start_urls[0]},
                                             meta={'art': art, 'brand': brand},
                                             wait_time=3,
                                             screenshot=True,
                                             callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        self.logger.info('sleeping 5s')
        time.sleep(5)
        self.logger.info('parsing {}'.format(art))
        brand = response.meta['brand']
        price = None
        if 'найден' not in response.text or 'запросу' not in response.text:
            return None
        try:
            title = response.css('div.widget-search-result-container').css('a.tile-hover-target')[1].css(
                'span::text').get()
            #if brand == 'frap':
            if art not in title:
                return None
            link = 'https://ozon.ru' + response.css('div.widget-search-result-container').css(
                'a.tile-hover-target::attr(href)').get().split('?')[0]
            for s in response.css('div.widget-search-result-container').css('div').css('span'):
                if 'style' in s.attrib:
                    if s.attrib['style'] in ['color:#f91155;',  'color:#001a34;']:
                        price = s.css('::text').get()
                        break
            if not price:
                return None
            price = price.replace('\u202f', '').replace('₽', '').replace(' ','')

            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': self.name,
                   'art': art
                   }
        except:
            raise
            pass
