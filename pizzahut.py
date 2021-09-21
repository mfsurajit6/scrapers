import random
import requests
from bs4 import BeautifulSoup
from constant import USER_AGENT


class PizzaHut:
    """ Get PizzaHut outlet information form all over United States in dictionary format"""
    def __init__(self):
        self.stores = {}
        self.state_urls = {}
        self.outlet_urls = []
        self.original_url = "https://locations.pizzahut.com/"
        self.headers = {
            'User-Agent': random.choice(USER_AGENT),
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }

    def get_stores(self):
        self.get_states()
        for s, l in self.state_urls.items():
            state_url = self.original_url+"/"+l
            res = requests.get(state_url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser')
            urls = soup.find_all("a", {"class": "Directory-listLink"})
            for u in urls:
                self.outlet_urls.append(u.get("href"))
        self.get_details()
        return self.stores

    def get_states(self):
        res = requests.get(self.original_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        state_data = soup.find("ul", {"class": "Directory-listLinks"})
        states = state_data.find_all("a", {"class": "Directory-listLink"})
        for a in states:
            state = a.text
            state_url = a.get("href")
            self.state_urls[state] = state_url

    def get_details(self):
        store_id = 1
        for u in self.outlet_urls:
            url = self.original_url+"/"+u
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser')
            outlets = soup.find_all("li", {"class": "Directory-listTeaser"})
            for outlet in outlets:
                store = {}
                store_address = outlet.find("span", {"class": "c-address-street-1"}).text
                store_address_1 = outlet.find("span", {"class": "c-address-street-2"})
                if store_address_1 is not None:
                    store_address += store_address_1.text
                store_phone = outlet.find("a", {"class": "c-phone-number-link c-phone-main-number-link"})
                store['name'] = outlet.find("span", {"class": "LocationName-geo"}).text
                store['address'] = store_address
                store['city'] = outlet.find("span", {"class": "c-address-city"}).text
                store['state'] = outlet.find("abbr", {"class": "c-address-state"}).text
                store['zip'] = outlet.find("span", {"class": "c-address-postal-code"}).text
                store['phone'] = store_phone.text if store_phone is not None else ''
                self.stores[store_id] = store
                store_id += 1


ph = PizzaHut()
print(ph.get_stores())
