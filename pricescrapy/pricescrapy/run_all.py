import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import sys
import os.path
import pandas as pd

process = CrawlerProcess(get_project_settings())
# print(process.settings['INPUT_FILENAME'][-14:-4])
outfile = process.settings['OUTPUT_FILENAME']
main_brand = process.settings['MAIN_BRAND']
if os.path.isfile(outfile):
    print(outfile)
    print('old')
    sys.exit()
file = open(outfile, 'w')
file.close()
group1 = ['8magazin', 'accessoriesforhome', 'cavevo', 'eldorado', 'guruvkusa', 'hoff', 'holodilnik', 'icecreamclub',
          'maxidom', 'mirposudy', 'msk-tescoma-posuda', 'projecthotel', 'tescoma-shop', 'tvoydom', 'variety-store',
          'vseblaga', 'wildberries', 'zelenyishar',]
group2 = ['posuda-pro', 'anuk', 'provance', 'provance-shop', 'myprovance', 'rposuda', 'masterglass', 'allrightshop',
          'bazaropt', 'axentia-shop', 'fg-buy', 'tdgaem', 'kibet-shop', 'goodstoria', 'just-tea', 'tea-vip',
          'coffeemanich', 'rusteaco', 'coffeespace', 'gutenberg', 'autocoffee', 'coffee-butik', 'kofe-kofe', 'mugduo',
          'posudarstvo', 'tea-coffee',
          ]
if main_brand == 'tescoma':
    for shop in group1:
        process.crawl(shop)
else:
    for shop in group2:
        process.crawl(shop)

process.start()  # the script will block here until all crawling jobs are finished

out_xls = process.settings['OUTPUT_XLSX_FILENAME']


def return_hyperlink(x):
    return '=HYPERLINK("{0}", {1})'.format(x['link'], x['price'])


df = pd.read_csv(outfile, delimiter=';', header=None,
                 names=['art', 'title', 'price', 'shop', 'link'])
df['shop_price'] = df.apply(return_hyperlink, axis=1)
dfp = pd.pivot_table(df, values=['shop_price'], index='art', columns='shop', aggfunc='first')
print(dfp.iloc[0, 3])
dfp.to_excel(out_xls)

file = open(outfile, 'a')
file.write("\nend of file\n")
file.close()

print("Done.")
