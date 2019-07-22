# encoding:UTF-8 

import requests
import bs4

url="https://news.yahoo.co.jp/topics/world"

data = requests.get(url)

soup = bs4.BeautifulSoup(data.text,'lxml')
li_list = soup("li", "newsFeed_item")

for li in li_list:
    title = li.find("div", "newsFeed_item_title")
    print(title)