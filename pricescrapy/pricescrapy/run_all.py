import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import sys
import os.path
#from spiders.mirposudy import MirposudySpider
#from spiders.posuda_pro import PosudaProSpider
#from spiders.projecthotel import ProjecthotelSpider
#from spiders.rposuda import RposudaSpider
#from spiders.masterglass import MasterglassSpider


t1 = os.path.getmtime('/tmp/uploads/input.txt')
t2 = os.path.getmtime('static/result.csv')
if t2>t1:
    print('old')
    sys.exit()
file = open('static/result.csv', 'w')
file.close()
process = CrawlerProcess(get_project_settings())
process.crawl('mirposudy')
process.crawl('posuda-pro')
process.crawl('projecthotel')
process.crawl('rposuda')
process.crawl('masterglass')
process.crawl('anuk')
process.crawl('provance')
process.crawl('provance-shop')
process.crawl('myprovance')
#process.crawl('lavandadecor')
process.start() # the script will block here until all crawling jobs are finished
print("Done.")
