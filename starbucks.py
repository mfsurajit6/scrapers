import random
import requests

from constant import ZIP_LAT_LANG, USER_AGENT
from urls import STARBUCKS_URL


class StarBucks:
    """ Get StarBucks outlet information form random locations of United States  in dictionary format"""
    def __init__(self):
        self.stores = {}
        self.base_url = STARBUCKS_URL
        self.headers = {
            "x-requested-with": "XMLHttpRequest",
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
        :return: dict, All Outlet Details
        """
        for i in range(len(ZIP_LAT_LANG)):
            lat = ZIP_LAT_LANG[i][1]
            long = ZIP_LAT_LANG[i][2]
            stores_from_location = self.get_data(lat, long)
            if stores_from_location != "Failed":
                for s in stores_from_location:
                    if s not in self.stores:
                        self.stores[s] = stores_from_location[s]
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
        url = f'{url}lat={lat}&lag={long}'
        # url += "lat=" + str(lat) + "&lag=" + str(long)
        try:
            res = requests.get(url, headers=self.headers)
            json_data = res.json()
        except Exception:
            return 'Failed'

        local_stores = json_data.get('stores')
        stores_data = {}

        for i in range(len(local_stores)):
            s = local_stores[i]
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


starbucks = StarBucks()
print(starbucks.get_stores())
