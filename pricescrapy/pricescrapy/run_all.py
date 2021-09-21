import configparser
import os.path
import sys
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def return_hyperlink(x):
    return '=HYPERLINK("{0}", {1})'.format(x['link'], x['price'])


process = CrawlerProcess(get_project_settings())
outfile = process.settings['OUTPUT_FILENAME']
main_brand = process.settings['MAIN_BRAND']
if os.path.isfile(outfile):
    print(outfile)
    print('old')
    os.remove(process.settings['IN_XLS_FILENAME'])
    sys.exit()
file = open(outfile, 'w')
file.close()
config = configparser.ConfigParser()
config.read('shops.cfg')
for shop, value in config.items('Shops'):
    if value == '1':
        if main_brand.lower() == 'frap':
            if shop in ('eldorado', 'mvideo'):
                continue
        elif main_brand.lower() == 'tescoma':
            if shop in ('wildberries'):
                continue
        print(shop)
        process.crawl(shop)

process.start()  # the script will block here until all crawling jobs are finished
#os.remove(process.settings['IN_XLS_FILENAME'])

out_xlsx = process.settings['OUTPUT_XLSX_FILENAME']

try:
    df = pd.read_csv(outfile, delimiter=';', header=None,
                     names=['art', 'title', 'price', 'shop', 'link'])
    df['shop_price'] = df.apply(return_hyperlink, axis=1)
    dfp = pd.pivot_table(df, values=['shop_price'], index='art', columns='shop', aggfunc='first')
    #print(dfp.iloc[0, 3])
    dfp.to_excel(out_xlsx)

    file = open(outfile, 'a')
    file.write("\nend of file\n")
    file.close()

    print("Done.")
except:
    print('nothing')
