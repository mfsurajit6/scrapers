import requests
from constant import ZIP_LAT_LANG


class StarBucks:
    def __init__(self):
        self.original_url = "https://www.starbucks.com/bff/locations?"
        self.url = ''

    def get_stores(self):
        data = {}
        for i in range(len(ZIP_LAT_LANG)):
            self.url = self.original_url
            lat = ZIP_LAT_LANG[i][1]
            long = ZIP_LAT_LANG[i][2]
            self.url += "lat="+str(lat)+"&lag="+str(long)
            print(self.url)
            stores = self.get_data(self.url)
            if stores != "Failed":
                for s in stores:
                    if s not in data:
                        data[s] = stores[s]
            else:
                print("Server is blocking...")
                return None
        return data

    def get_data(self, url):
        headers = {
            "x-requested-with": "XMLHttpRequest"
        }
        res = requests.get(self.url, headers=headers)
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
            # print(address)
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
