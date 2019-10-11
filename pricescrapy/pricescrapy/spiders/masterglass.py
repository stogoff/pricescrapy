# -*- coding: utf-8 -*-
import scrapy


class MasterglassSpider(scrapy.Spider):
    name = 'masterglass'
    allowed_domains = ['masterglass.ru']

    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].replace(',', '.').replace('.00', '').strip()
                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'http://masterglass.ru/index.php'
                data = {'m':'catalog','mode' :'l','ajax':'1','str':art}
                yield scrapy.http.FormRequest(url=url, meta={'art': art}, formdata=data, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        trows = response.css('tr')
        shop = self.name
        if len(trows)>1:
            tr = trows[1]
            try:
                if art in tr.css('td')[3].css('font::text').get():
                    title = tr.css('td')[1].css('a::text').get()
                    link = 'https://projecthotel.ru' + tr.css('td')[1].css('a').xpath('@href').get()

                    price = tr.css('td')[6].css('a::text').get().strip()
                    #price = re.sub(r'\,', '', price)
                    # price = re.match(r'\d+', price).group(0)
                    yield {'title': title,
                           'link': link,
                           'price': price,
                           'shop': shop,
                           'art': art
                           }
            except:
                pass
