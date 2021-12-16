from bs4 import BeautifulSoup
import requests
import unicodedata
import time

def infoget(recurl):

  hinta = ""
  info = []
  final = []

  page = requests.get(recurl)
  soup = BeautifulSoup(page.content, 'html.parser')


  if soup.find_all("div", {"class": "column tiny-12 medium-6 padding-t-5 padding-h-0"}):
    return "error"


  name = soup.find("h1", {"class": "product-name"}).get_text()
  volume = soup.find("span", {"class": "volume"}).get_text()
  volume = volume.replace(u'\xa0', u' ')

  userdata = { name:[]}

  for child in soup.find_all("span", {"class": "price-part"}):
    hinta += child.get_text() + "."

  hinta = hinta[:-1]

  soup = soup.find("div", {"class": "hard-facts"})

  for child in soup.find_all("li"):
    for child2 in child.find_all("div"):
      info.append(child2.get_text(strip=True))

  v = ''
  for x in info:
    y = x.replace(u'\n', u' ')
    v = y.replace(u'\xa0', u' ')
    final.append(v)

  tempp = recurl.replace('https://www.alko.fi/tuotteet/', '')
  loop = 1
  x = {}
  x["nimi"] = name
  x["hinta"] = hinta
  x["maara"] = volume
  x["thumbnail"] = "https://images.alko.fi/images/cs_srgb,f_auto,t_products/cdn/" + tempp[:-1] +".jpg"
  x["fullimage"] = "https://images.alko.fi/images/cs_srgb,f_auto,t_medium/cdn/" + tempp[:-1] +".jpg"
  while (loop < (len(final))):
    x[final[loop-1]] = final[loop]
    loop = loop + 2

  userdata[name].append(x)

  #userdata[name]["thumbnail"].append("https://images.alko.fi/images/cs_srgb,f_auto,t_products/cdn/" + tempp[:-1] +".jpg")
  #userdata[name]["fullimage"].append("https://images.alko.fi/images/cs_srgb,f_auto,t_medium/cdn/" + tempp[:-1] +".jpg")
  #userdata[name].append("https://images.alko.fi/images/cs_srgb,f_auto,t_products/cdn/" + tempp[:-1] +".jpg")
  #userdata[name].append("https://images.alko.fi/images/cs_srgb,f_auto,t_medium/cdn/" + tempp[:-1] +".jpg")

  return userdata

def aika():
  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  return '[' + current_time + '] '
