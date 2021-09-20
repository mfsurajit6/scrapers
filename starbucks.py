import random
import requests
from constant import ZIP_LAT_LANG, USER_AGENT


class StarBucks:
    """ Get StarBucks outlet information form random locations of United States  in dictionary format"""
    def __init__(self):
        self.original_url = "https://www.starbucks.com/bff/locations?"
        self.headers = {
            "x-requested-with": "XMLHttpRequest",
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
            url += "lat="+str(lat)+"&lag="+str(long)
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
        res = requests.get(url, headers=self.headers)
        # print(res.text)
        try:
            data = res.json()
        except ValueError:
            return 'Failed'

        stores = data.get('stores')
        stores_data = {}

        for i in range(len(stores)):
            s = stores[i]
            store = {}
            store_id = s.get('id')
            store['name'] = s.get('name')
            address = s.get('address')
            store['address'] = address.get('streetAddressLine1')
            store['city'] = address.get('city')
            store['state'] = address.get('countrySubdivisionCode')
            store['zip'] = address.get('postalCode')
            store['phone'] = s.get('phoneNumber')
            store['latitude'] = s['coordinates']['latitude']
            store['longitude'] = s['coordinates']['longitude']

            if store_id not in stores_data.keys():
                stores_data[store_id] = store

        return stores_data


v = StarBucks()
print(v.get_stores())
