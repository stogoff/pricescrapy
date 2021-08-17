from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
#chrome_options.add_argument(f'--proxy-server=194.233.69.38:443')
driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.iplocation.net/'
    #'https://www.citilink.ru/search/?text=Frap+F4101-12'
    #'https://www.wildberries.ru/catalog/0/search.aspx?xparams=search%3Dfrap+f1052-56&xshard=&sort=popular&search=Frap+F1052-56'


driver.get(url)
art = 0
print(1)
for x in range(2):
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_UP)
    actions.perform()
    time.sleep(.5)
driver.get_screenshot_as_file('image.png')
html = driver.page_source
soup = bs(html, "html.parser")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f'--proxy-server=194.233.69.38:443')
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
print(2)
for x in range(2):
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_UP)
    actions.perform()
    time.sleep(.5)
driver.get_screenshot_as_file('image_p.png')
html = driver.page_source

#coms = soup.find_all('a', class_='ref_goods_n_p j-open-full-product-card')
#link = soup.select('a.j-open-full-product-card.ref_goods_n_p')[0].get('href').split('?')[0]
#result_text = soup.select('p.searching-results-text')
#print(soup.select('p.searching-results-text')[0].parent.get('class'))
#return link

