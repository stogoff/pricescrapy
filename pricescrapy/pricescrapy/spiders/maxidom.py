# -*- coding: utf-8 -*-
import scrapy
import re

class MaxidomSpider(scrapy.Spider):
    name = 'maxidom'
    allowed_domains = ['maxidom.ru']
    start_urls = ['http://maxidom.ru/']


    def start_requests(self):
        with open(self.settings['INPUT_FILENAME']) as f:
            for line in f.readlines():
                # print(line.strip().split(';'))

                brand = line.strip().split(';')[0]
                art = line.strip().split(';')[1].split('.')[0].split(',')[0]

                title = line.strip().split(';')[2]
                # query = "{} {}".format(art,title)
                print(art)
                url = 'https://www.maxidom.ru/search/catalog/?q={}+{}&category_search=0'.format(brand,art)
                yield scrapy.Request(url=url, meta={'art': art}, callback=self.parse)

    def parse(self, response):
        art = response.meta['art']
        for ar in response.css('article.item-list'):
            div = ar.css('div.caption-list')
            if art in div.css('small.sku::text').get():

                title = div.css('a::text').get()


                link = 'https://www.maxidom.ru' + div.css('a').xpath('@href').get()
                shop = self.name
                info = ar.css('div.info')
                price = info.css('div.price').css('span::text').get()
                price = re.sub(r'\s+', '', price)
                price = re.match(r'\d+', price).group(0)
                yield {'title': title,
                           'link': link,
                           'price': price,
                           'shop': shop,
                           'art': art
                           }
"""
                <article itemscope="" itemtype="http://schema.org/Product" class="item-list group">
                    <div class="item-list-ico">
                                                                                            </div>

                                        <figure>
                        <a class="img_href" href="/catalog/nabory-kukhonnykh-instrumentov/1000735248/" onclick="productClick('5',{'id':'','name':'5','price':'5','category_id':'','category_name':'5'},{'id':'spb','name':'5','price':'5','category_id':'41498','category_name':'5'});">
                            <img itemprop="image" src="/upload/iblock/da9/da9f0932eb826982b78e56e32c1eba4a.jpg" alt="набор кухонных аксессуаров TESCOMA Woody, 3 шт, дерево">
                        </a>
                    </figure>
                    <div class="caption-list">
                        <a itemprop="name" href="/catalog/nabory-kukhonnykh-instrumentov/1000735248/" onclick="productClick('5',{'id':'','name':'5','price':'5','category_id':'','category_name':'5'},{'id':'spb','name':'5','price':'5','category_id':'41498','category_name':'5'});" class="name-big">набор кухонных аксессуаров TESCOMA Woody, 3 шт, дерево</a>
                        <div class="small-top" itemprop="description">
                            <small class="sku">Артикул: 637418</small>
                            <small class="sku">Код товара: 1000735248</small>
                                                            <small class="sku">Торговая марка: TESCOMA</small>
                                                                                </div>
                        <p class="item-caption">
                                                    </p>

                        <div class="small-bottom">
                                                                                        <small class="sku">
                                                                                                                Чехия                                                                    </small>
                                                                                        <small class="sku">0.11                                    кг
                                </small>
                                                                                </div>
                        <div class="item-controls">
                                                        <span class="stock instock">В наличии</span>
                                                        <a href="#" class="compare-inline" data-id="5276741"><span class="active">К сравнению</span><span>В сравнении</span></a>
                                                    </div>
                    </div>

                    <div class="wrap-buy" itemprop="offers" itemscope="" itemtype="http://schema.org/Offer">
                        <meta itemprop="priceCurrency" content="RUB">
                        <div class="bl_prd_price">
                            <span class="price-older">
                                                            </span>
                            <span class="price-list">
                                <span data-repid_price="359">359,-</span>
                                <span style="display: none" itemprop="price">359</span>
                                
                            </span>
                            

                            <div class="bl_prod_action_info"></div>

                                                    </div>


                                                    <div class="number-wrap">
                                <div class="number">
                                    <button class="minus"></button>
                                    <input type="text" class="counter" value="1">
                                    <button class="plus"></button>
                                </div>
                                                                    <span class="measure">
                                        шт.                                    </span>
                                                            </div>
                            <div class="bl_prd_buttom">
                                <button type="submit" class="button button-cart" hlink="/catalog/nabory-kukhonnykh-instrumentov/1000735248/" minquant="1" repid="5277162" onclick="add2basket_catalog('5',{'id':'','name':'5','price':'5','category_id':'','category_name':'5'},{'id':'spb','name':'5','price':'5','category_id':'41498','category_name':'5'});">В корзину
                                </button>
                            <div style="position: relative">
                                <div class="popup-box popup-box-cart hidden">
                                    <div class="arr"></div>

                                    
                                    <div class="popup-cart">
                                        <h3>Товар добавлен в корзину</h3>
                                        <div class="img">
                                            <img src="/upload/iblock/da9/da9f0932eb826982b78e56e32c1eba4a.jpg" alt="набор кухонных аксессуаров TESCOMA Woody, 3 шт, дерево">
                                        </div>
                                        <div class="info">
                                            <div class="name-item">набор кухонных аксессуаров TESCOMA Woody, 3 шт, дерево</div>
                                            <div class="count">Количество: <span>1</span> шт.                                                                                            </div>
                                            <div style="display: none;" id="once_item_price">359</div>
                                            <div class="price">Стоимость: <span>359,-</span></div>
                                            <div class="price-older">
                                                                                            </div>
                                        </div>

                                        <div class="clear"></div>
                                        <form action="/personal/cart/" style="display: inline;">
                                            <button type="submit" class="button button-popup-cart" onsubmit="getToBasketHandler('5');">Перейти в корзину</button>
                                        </form>
                                        <button type="button" class="button-light button-popup-cart close-popup-cart">Продолжить
                                            покупки
                                        </button>
                                    </div>
                                    <i class="cross-popup"></i>
                                </div>
                            </div>
                            </div>
                                            </div>
                </article>
                """
