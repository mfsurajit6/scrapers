import random
import requests
import json

from constant import ZIP_LAT_LANG, USER_AGENT


class Verizon:
    """ Get Verizon outlet information form random locations of United States  in dictionary format"""
    def __init__(self):
        # "https://www.verizon.com/stores/searchresultsdata?lat=38.9071923&long=-77.0368707"
        self.original_url = "https://www.verizon.com/stores/searchresultsdata?"
        self.headers = {
            'User-Agent': random.choice(USER_AGENT),
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }
        self.data = {}

    def get_stores(self):
        for i in range(len(ZIP_LAT_LANG)):
            url = self.original_url
            lat = ZIP_LAT_LANG[i][1]
            long = ZIP_LAT_LANG[i][2]
            url += "lat=" + str(lat) + "&long=" + str(long)
            stores = self.get_data(url)
            if stores != "Failed":
                for s in stores:
                    if s not in self.data:
                        self.data[s] = stores[s]
            else:
                print("Server is blocking...")
                return None
        return self.data

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        stores = json.loads(response.content)
        stores_data = {}
        for s in stores:
            if isinstance(s, str):
                continue
            store = {}
            store['name'] = s.get('storeName')
            store['address'] = s.get('address')
            store['city'] = s.get('city')
            store['state'] = s.get('state')
            store['zip'] = s.get('zip')
            store['phone'] = s.get('phone')
            store['latitude'] = s.get('lat')
            store['longitude'] = s.get('lng')
            store_number = s.get('storeNumber')
            if store_number not in stores_data:
                stores_data[store_number] = store
        return stores_data


v = Verizon()
print(v.get_stores())
