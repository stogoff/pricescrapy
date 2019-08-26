# -*- coding: utf-8 -*-
import scrapy


class AnukSpider(scrapy.Spider):
    name = 'anuk'
    allowed_domains = ['anuk-anuk.com']
    start_urls = ['http://anuk-anuk.com/']

    def parse(self, response):
        pass
