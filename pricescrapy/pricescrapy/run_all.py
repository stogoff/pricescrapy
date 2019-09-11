import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import sys
import os.path
import pandas as pd


process = CrawlerProcess(get_project_settings())
# print(process.settings['INPUT_FILENAME'][-14:-4])
outfile = process.settings['OUTPUT_FILENAME']
if os.path.isfile(outfile):
    print(outfile)
    print('old')
    sys.exit()
file = open(outfile, 'w')
file.close()
process.crawl('mirposudy')
process.crawl('posuda-pro')
process.crawl('projecthotel')
process.crawl('rposuda')
process.crawl('masterglass')
process.crawl('anuk')
process.crawl('provance')
process.crawl('provance-shop')
process.crawl('myprovance')
# process.crawl('lavandadecor')
process.crawl('tvoydom')
process.crawl('maxidom')

process.crawl('hoff')
process.crawl('accessoriesforhome')
process.crawl('tescoma-shop')
process.crawl('holodilnik')
process.crawl('eldorado')

process.crawl('wildberries')
process.crawl('allrightshop')
process.crawl('bazaropt')
process.crawl('axentia-shop')
process.crawl('vseblaga')
process.crawl('cavevo')
process.crawl('fg-buy')
process.crawl('tdgaem')
process.crawl('kibet-shop')
process.crawl('goodstoria')
process.crawl('icecreamclub')
process.crawl('msk-tescoma-posuda')
process.crawl('variety-store')
process.crawl('zelenyishar')
process.crawl('guruvkusa')
process.crawl('8magazin')
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
