import csv
import requests
import pandas as pd

from bs4 import BeautifulSoup

brands = []
names = []
prices = []
shopping_links = []

url = "https://www.flipkart.com/search?q=watch&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
watches = soup.find_all("div", {"class": "_1xHGtK _373qXS"})
for watch in watches:
    brand = watch.find("div", {"class": "_2WkVRV"})
    name = watch.find("a", {"class": "IRpwTa"})
    price = watch.find("div", {"class": "_30jeq3"})
    shopping_link = watch.find("a", {"class": "_3bPFwb"})
    # print(shopping_link.get('href'))
    brands.append(brand.text)
    names.append(name.text)
    prices.append(price.text)
    shopping_links.append("https://www.flipkart.com" + shopping_link.get('href'))

df = pd.DataFrame({"Watch Name": names, "Brand": brands, "Price": prices, "Shopping Link": shopping_links})
print(df.head())
df.to_csv("Watches.csv")
