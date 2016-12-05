import googlemaps
from datetime import datetime


"""
start_address
list keywords
time range
budget rating

"""

PLACES_KEY = 'AIzaSyDg1qhBCO1I7heUbEfXKM4OSNO_EG7P-mw'
MAPS_KEY = 'AIzaSyCPzQ7BurH64jXtsgwP7c7VQBK8LQPF5MY'

def collectData(user_data):

    places = {keyword: [] for keyword in user_data['keywords']}

    places_client = googlemaps.Client(key=PLACES_KEY)

    geocode_client = googlemaps.Client(key=MAPS_KEY)
    geocode = geocode_client.geocode(user_data['start_address'])
    geocode_tup = (geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng'])

    for keyword in places:
        data = places_client.places_nearby(
            geocode_tup,
            min_price=0,
            max_price=4,
            type=keyword,
            open_now=True,
            radius=5000,
        )
        for p in data["results"]:
            placeStats = places_client.place(p["place_id"])
            rating = None 
            try:
                rating = placeStats["result"]["rating"]
            except KeyError:
                rating = 0

            geocode = geocode_client.geocode(placeStats["result"]["formatted_address"])
            geo_tup = (geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng'])

            newItem = {
                'name':  p["name"],
                'opening_hours':  p["opening_hours"],
                'price_level':  p["price_level"],
                'rating': rating,
                'address': placeStats["result"]["formatted_address"],
                'geo_loc': geo_tup,
            }
            places[keyword].append(newItem)
    print(places)


test_data = {'start_address': '1769 Rockies Ct, Lafayette, CO', 'keywords': ['restaurant', 'cafe']}

collectData(test_data)
            
