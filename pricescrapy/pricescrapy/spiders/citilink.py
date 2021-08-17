import scrapy
import time
from scrapy_selenium import SeleniumRequest


class CitilinkSpider(scrapy.Spider):
    name = 'citilink'
    allowed_domains = ['citilink.ru']
    start_urls = ['http://citilink.ru/']
    search = 'https://www.citilink.ru/search/?text={}+{}'

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                time.sleep(2)
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
                                             wait_time=3,
                                             screenshot=True,
                                             callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        brand = response.meta['brand']
        try:
            try:
                na = response.css('h2.ProductHeader__not-available-header::text').get().strip()
                self.logger.info('{} is not available'.format(art))
                return None
            except:
                pass
            t = response.css('div.ProductCardVerticalLayout')[0]
            link = 'https://citilink.ru' + t.css('a.ProductCardVertical__name::attr(href)').get()
            title = t.css('a.ProductCardVertical__name::attr(title)').get()
            if art.lower() not in title.lower():
                self.logger.info('{} !!!=== {}'.format(art, title))
                return None
            try:
                price = t.css('span.ProductCardVerticalPrice__price-club_current-price::text').get().strip()
            except AttributeError:
                try:
                    price = t.css('span.ProductCardVerticalPrice__price-current_current-price::text').get().strip()
                except AttributeError:
                    return None

            yield {'title': title,
                   'link': link,
                   'price': price,
                   'shop': self.name,
                   'art': art
                   }
        except:
            self.logger.error('{} parsing error'.format(art))
            raise
