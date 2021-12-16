from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import infoscraper
from infoscraper import aika
import sys
import os



options = Options()
options.headless = True

url = ""
s=Service('C:\Windows\geckodriver.exe')
driver = webdriver.Firefox(options=options, service=s)

if (len(sys.argv)) > 0:
    url = sys.argv[1]
else:
    sys.exit(0)

path1 = sys.argv[0].replace('main.py', '')


name = url.replace('https://www.alko.fi/tuotteet/', '')


driver.get(url)
time.sleep(2)  
scroll_pause_time = 1 
screen_height = driver.execute_script("return window.screen.height;")   
i = 1

print(aika() + "started scrolling")

while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break

print(aika() + "finished scrolling")

urls = []
soup = BeautifulSoup(driver.page_source, "html.parser")
for parent in soup.find_all(class_="js-product-link"):
    urls.append(parent.attrs['href'])

driver.quit()
print(aika() + "Exiting driver")

print(aika() + "scraping info from urls")

finaldata = { "data":[]}

if not os.path.exists('output'):
    os.makedirs('output')

path1 += 'output\\'

for x in urls:
        print(aika() + x)
        finaldata["data"].append(infoscraper.infoget(x))
        time.sleep(1)

with open(path1 + name + '.json', 'w') as filehandle:
    json.dump(finaldata, filehandle)


print(aika() + "Successfully crawled " + str(len(urls)) + " urls!")



