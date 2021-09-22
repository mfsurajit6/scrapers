import random
import requests
import json

from constant import ZIP_LAT_LANG, USER_AGENT
from urls import VERIZON_URL


class Verizon:
    """ Get Verizon outlet information form random locations of United States  in dictionary format"""
    def __init__(self):
        self.base_url = VERIZON_URL
        self.headers = {
            'User-Agent': random.choice(USER_AGENT),
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }
        self.stores = {}

    def get_stores(self):
        """
        Get all the outlet details
        :return: dict, All Outlet Details
        """
        for i in range(len(ZIP_LAT_LANG)):
            lat = ZIP_LAT_LANG[i][1]
            long = ZIP_LAT_LANG[i][2]
            local_stores = self.get_data(lat, long)
            if local_stores != "Failed":
                for s in local_stores:
                    if s not in self.stores:
                        self.stores[s] = local_stores[s]
            else:
                print("Server is blocking...")
                return None
        return self.stores

    def get_data(self, lat, long):
        """
        Get Outlet Details of specific location
        :param lat: float, Latitude of the location
        :param long: float, Longitude of the location
        :return: dict, Stores of the specified location
        """
        url = self.base_url
        url = f'{url}lat={lat}&long={long}'
        try:
            response = requests.get(url, headers=self.headers)
            local_stores = json.loads(response.content)
        except Exception:
            return 'Failed'

        stores_data = {}
        for local_store in local_stores:
            if isinstance(local_store, str):
                continue
            store = {}
            store['name'] = local_store.get('storeName')
            store['address'] = local_store.get('address')
            store['city'] = local_store.get('city')
            store['state'] = local_store.get('state')
            store['zip'] = local_store.get('zip')
            store['phone'] = local_store.get('phone')
            store['latitude'] = local_store.get('lat')
            store['longitude'] = local_store.get('lng')
            store_number = local_store.get('storeNumber')
            if store_number not in stores_data:
                stores_data[store_number] = store
        return stores_data


verizon = Verizon()
print(verizon.get_stores())
