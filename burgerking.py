import random
import requests

from constant import ZIP_LAT_LANG, USER_AGENT
from urls import BURGERKING_URL


class BurgerKing:
    """ Get BurgerKing outlet information form random locations of United States  in dictionary format"""
    def __init__(self):
        self.stores = {}
        self.url = BURGERKING_URL
        self.query = """
                query GetRestaurants($input: RestaurantsInput) {  restaurants(input: $input) {    pageInfo {      hasNextPage      endCursor      __typename    }    totalCount    nodes {      ...RestaurantNodeFragment      __typename    }    __typename  }}fragment RestaurantNodeFragment on RestaurantNode {  _id  storeId  isAvailable  posVendor  chaseMerchantId  curbsideHours {    ...OperatingHoursFragment    __typename  }  deliveryHours {    ...OperatingHoursFragment    __typename  }  diningRoomHours {    ...OperatingHoursFragment    __typename  }  distanceInMiles  drinkStationType  driveThruHours {    ...OperatingHoursFragment    __typename  }  driveThruLaneType  email  environment  franchiseGroupId  franchiseGroupName  frontCounterClosed  hasBreakfast  hasBurgersForBreakfast  hasCatering  hasCurbside  hasDelivery  hasDineIn  hasDriveThru  hasMobileOrdering  hasParking  hasPlayground  hasTakeOut  hasWifi  id  isDarkKitchen  isFavorite  isRecent  latitude  longitude  mobileOrderingStatus  name  number  parkingType  phoneNumber  physicalAddress {    address1    address2    city    country    postalCode    stateProvince    stateProvinceShort    __typename  }  playgroundType  pos {    vendor    __typename  }  posRestaurantId  restaurantImage {    asset {      _id      metadata {        lqip        palette {          dominant {            background            foreground            __typename          }          __typename        }        __typename      }      __typename    }    crop {      top      bottom      left      right      __typename    }    hotspot {      height      width      x      y      __typename    }    __typename  }  restaurantPosData {    _id    __typename  }  status  vatNumber  __typename}fragment OperatingHoursFragment on OperatingHours {  friClose  friOpen  monClose  monOpen  satClose  satOpen  sunClose  sunOpen  thrClose  thrOpen  tueClose  tueOpen  wedClose  wedOpen  __typename}
                """
        self.variables = {
            "input": {
                "filter": "NEARBY",
                "coordinates": {
                    "userLat": 0,
                    "userLng": 0,
                    "searchRadius": 32000
                },
                "first": 20,
                "status": "OPEN"
            }
        }
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
        :return: dict, All Outlet Details
        """
        for i in range(len(ZIP_LAT_LANG)):
            lat = ZIP_LAT_LANG[i][1]
            long = ZIP_LAT_LANG[i][2]
            stores_from_location = self.get_details(lat, long)
            if stores_from_location != "Failed":
                for store in stores_from_location:
                    if store not in self.stores:
                        self.stores[store] = stores_from_location[store]
            else:
                print("Server is blocking...")
                return None
        return self.stores

    def get_details(self, lat, long):
        """
        Get Outlet Details of specific location
        :param lat: float, Latitude of the location
        :param long: float, Longitude of the location
        :return: dict, Stores of the specified location
        """
        local_stores = {}
        self.variables["input"]["coordinates"]["userLat"] = lat
        self.variables["input"]["coordinates"]["userLng"] = long
        try:
            response = requests.post(self.url, json={'query': self.query, 'variables': self.variables}, headers=self.headers)
            json_data = response.json()
            nodes = json_data.get("data").get("restaurants").get("nodes")
        except Exception:
            return None
        for node in nodes:
            store = {}
            store_id = node.get("storeId")
            store_name_long = node.get("name")
            physical_address = node.get("physicalAddress")
            store_address = physical_address.get("address1")
            store_address += physical_address.get("address2") if physical_address.get("address2") != "" else ""
            store["name"] = store_name_long.split(',')[0]
            store["address"] = store_address
            store["city"] = physical_address.get("city")
            store["state"] = physical_address.get("stateProvince")
            store["zip"] = physical_address.get("postalCode").split("-")[0]
            store["phone"] = node.get("phoneNumber")
            store["latitude"] = node.get("latitude")
            store["longitude"] = node.get("longitude")
            if store_id not in local_stores:
                local_stores[store_id] = store
        return local_stores


burgerking = BurgerKing()
print(burgerking.get_stores())
