import random
import requests
from bs4 import BeautifulSoup

from constant import USER_AGENT
from urls import PIZZAHUT_URL


class PizzaHut:
    """ Get PizzaHut outlet information form all over United States in dictionary format"""

    def __init__(self):
        self.stores = {}
        self.state_urls = {}
        self.outlet_urls = []
        self.base_url = PIZZAHUT_URL
        self.headers = {
            'User-Agent': random.choice(USER_AGENT),
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }

    def get_stores(self):
        """
        Get all the outlet details
        :return: dict, All Store Details
        """
        self.get_states()
        for state, link in self.state_urls.items():
            # url = f'{url}lat={lat}&long={long}'
            state_url = f'{self.base_url}/{link}'
            # state_url = self.base_url + "/" + link
            res = requests.get(state_url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser')
            urls = soup.find_all("a", {"class": "Directory-listLink"})
            for url in urls:
                self.outlet_urls.append(url.get("href"))
        self.get_details()
        return self.stores

    def get_states(self):
        """
        Finds the states and corresponding URLS and put it in state_urls list
        :return: None
       """
        res = requests.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        state_data = soup.find("ul", {"class": "Directory-listLinks"})
        states = state_data.find_all("a", {"class": "Directory-listLink"})
        for a in states:
            state = a.text
            state_url = a.get("href")
            self.state_urls[state] = state_url

    def get_details(self):
        """
        Find the outlet of evey states
        :return: None
        """
        store_id = 1
        for outleturl in self.outlet_urls:
            url = self.base_url + "/" + outleturl
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


pizzahut = PizzaHut()
print(pizzahut.get_stores())
