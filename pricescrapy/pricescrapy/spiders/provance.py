# -*- coding: utf-8 -*-
import scrapy


class ProvanceSpider(scrapy.Spider):
    name = 'provance'
    allowed_domains = ['provance.ru']
    start_urls = ['http://provance.ru/']

    def parse(self, response):
        pass
