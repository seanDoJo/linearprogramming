import googlemaps
import datetime


PLACES_KEY = 'AIzaSyDg1qhBCO1I7heUbEfXKM4OSNO_EG7P-mw'
PLACES_KEY = 'AIzaSyBD5fNjnMJ2vo_jWsz1x3fWXrcRb4TOAJ0'

#MAPS_KEY = 'AIzaSyCPzQ7BurH64jXtsgwP7c7VQBK8LQPF5MY'
#MAPS_KEY = 'AIzaSyCPLE1prImwt1JXgbdtwfomzfiqr5bO1us'
#MAPS_KEY = 'AIzaSyC-FkHdIYrMklmF2VwKJUgJU5xVoJEd0nw'
#MAPS_KEY = 'AIzaSyDwa9wQN2Co8owZX6VaLRm9L9B7XQj6Svk'
#MAPS_KEY = 'AIzaSyCeRAPsVxCpJsUzWfJMxLAagpe4VeoL-8Y'
#MAPS_KEY = 'AIzaSyDW3rShVk6rPbo8CzZ3UbJ5NJEAu2hVz-k'
#MAPS_KEY = 'AIzaSyAWR52HC7ZOTkkXW0Clpzm0dT_NXo4g1vs'
MAPS_KEY = 'AIzaSyAp2R3_jPn_So3xm8ljiZUMSqbFCCMClYo'

def collectData(user_data):
    all_data = {}
    place_data = collectUserData(user_data)
    distance_data = collectMapData(place_data)

    all_data["user_data"] = user_data
    all_data["place_data"] = place_data
    all_data["distance_data"] = distance_data

    return all_data

def collectMapData(place_data):
    distance_data = {}

    glob_place_data = [ place_data[k] for k in place_data ]
    glob_place_data = [ (item["name"], item["address"], item["geo_loc"]) for row in glob_place_data for item in row ]
    maps_client = googlemaps.Client(key=MAPS_KEY)

    frm = []
    to = []
    origins = []
    destinations = []

    for i in range(len(glob_place_data)):
        name1, address1, loc1 = glob_place_data[i]
        for j in range(i+1, len(glob_place_data)):
                name2, address2, loc2 = glob_place_data[j]
                to.append(name1)
                frm.append(name2)
                origins.append(address1)
                destinations.append(address2)

    for j in range(0, len(origins), 10):
        print(len(origins[j:min(j+10, len(origins))]))
        dest_data = maps_client.distance_matrix(
            origins[j:min(j+10, len(origins))], 
            destinations[j:min(j+10, len(origins))]
        )

        for i in range(len(dest_data["rows"])):
            d = dest_data["rows"][i]
            fromName = frm[j+i]
            toName = to[j+i]
            distance_data[(fromName, toName)] = 30 +  d["elements"][0]["duration"]["value"]
            distance_data[(toName, fromName)] = 30 +  d["elements"][0]["duration"]["value"]
    return distance_data


def collectUserData(user_data):
    
    current_day = datetime.datetime.today().weekday()
    if current_day == 6:
        current_day = 0
    else:
        current_day += 1
    
    places = {keyword: [] for keyword in user_data['keywords'] + ["HOME"]}

    places_client = googlemaps.Client(key=PLACES_KEY)

    geocode_client = googlemaps.Client(key=MAPS_KEY)
    geocode = geocode_client.geocode(user_data['start_address'])
    
    geocode_tup = (geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng'])
    da = geocode_client.reverse_geocode(geocode_tup)
    home_addr = da[0]["formatted_address"]
    homeItem = {
        'name':  "HOME",
        'opening_hours':  (0, 2359),
        'price_level':  0,
        'rating': 0,
        'address': home_addr,
        'geo_loc': geocode_tup,
    }
    places["HOME"].append(homeItem)

    seen_places = []

    for keyword in user_data['keywords']:
        key_weight = user_data["weights"][keyword]
        data = places_client.places_nearby(
            geocode_tup,
            min_price=0,
            max_price=4,
            type=keyword,
            open_now=True,
            radius=user_data['radius'],
        )
        for p in data["results"]:
            placeStats = places_client.place(p["place_id"])

            rating = None 
            try:
                rating = placeStats["result"]["rating"]
                rating = rating * key_weight
            except KeyError:
                rating = 0

            trange = (0, None)
            try:
                opening_hours = placeStats["result"]["opening_hours"]["periods"]
                for day in opening_hours:
                    if day["open"]["day"] == current_day:
                        opening = int(day["open"]["time"])
                        closing = None
                        if (day["close"]["time"] is not None):
                            closing = int(day["close"]["time"]) 
                        trange = (opening, closing)
                        break
            except KeyError:
                pass

            timeOk = True
            
            if (trange[1] is not None):
                n = datetime.datetime.now().time()
                nowTime = (n.hour*100) +  n.minute
                dur = user_data["time"]
                durHour = dur / 3600
                durMin = (dur - (durHour * 3600)) / 60
                durr = (durHour * 100) + durMin
                if trange[1] < trange[0]:
                    if (nowTime + durr) >= 2400:
                        durr = (nowTime + durr) % 2400
                        if durr > trange[1]:
                            timeOk = False
                else:   
                    timeOk = ((nowTime + durr) <= trange[1])

            geocode = geocode_client.geocode(placeStats["result"]["formatted_address"])
            if (len(geocode) > 0 and timeOk):
                if ((p["name"], placeStats["result"]["formatted_address"]) not in seen_places):
                    geo_tup = (geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng'])

                    newItem = {
                        'name':  p["name"]+" ("+placeStats["result"]["formatted_address"].replace(",", "")+")",
                        'opening_hours':  trange,
                        'price_level':  p["price_level"],
                        'rating': rating,
                        'address': placeStats["result"]["formatted_address"],
                        'geo_loc': geo_tup,
                    }
                    places[keyword].append(newItem)
                    seen_places.append((p["name"], placeStats["result"]["formatted_address"]))
        #places[keyword] = places[keyword][:5]

    return places
