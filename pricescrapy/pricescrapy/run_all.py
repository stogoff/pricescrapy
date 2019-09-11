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
if main_brand == 'tescoma':
    process.crawl('8magazin')
    process.crawl('accessoriesforhome')
    process.crawl('cavevo')
    process.crawl('eldorado')
    process.crawl('guruvkusa')
    process.crawl('hoff')
    process.crawl('holodilnik')
    process.crawl('icecreamclub')
    process.crawl('maxidom')
    process.crawl('msk-tescoma-posuda')
    process.crawl('tescoma-shop')
    process.crawl('tvoydom')
    process.crawl('variety-store')
    process.crawl('vseblaga')
    process.crawl('wildberries')
    process.crawl('zelenyishar')
    process.crawl('mirposudy')
    process.crawl('projecthotel')
else:
    process.crawl('posuda-pro')
    process.crawl('anuk')
    process.crawl('provance')
    process.crawl('provance-shop')
    process.crawl('myprovance')
    process.crawl('rposuda')
    process.crawl('masterglass')
    process.crawl('allrightshop')
    process.crawl('bazaropt')
    process.crawl('axentia-shop')
    process.crawl('fg-buy')
    process.crawl('tdgaem')
    process.crawl('kibet-shop')
    process.crawl('goodstoria')
    process.crawl('just-tea')
    process.crawl('tea-vip')
    process.crawl('coffeemanich')
    process.crawl('rusteaco')
    process.crawl('coffeespace')
    process.crawl('gutenberg')
# process.crawl()
# process.crawl()
# process.crawl()
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
