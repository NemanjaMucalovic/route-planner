import googlemaps
import os


api_key = os.environ.get('MAPS_API_KEY')
gmaps = googlemaps.Client(key=api_key)

def convert_location_to_geocode(location):
    result = gmaps.geocode(location)
    return result[0]['geometry']['location']

def get_places(location, place_type):
    geocoded_location = convert_location_to_geocode(location)
    places_raw = gmaps.places_nearby(location=geocoded_location, type=place_type, radius=5000)
    places_unfiltered = places_raw['results']
    places = []
    for place in places_unfiltered:
        place_info = {
                "business_status" : place.get("business_status", "N/A"),
                "is_opened": place.get("opening_hours",{}).get("open_now", "N/A"),
                "lat": place["geometry"]["location"].get("lat","N/A"),
                "lng": place["geometry"]["location"].get("lng","N/A"),
                "name": place.get("name"),
                "user_ratings_total" : place.get("user_ratings_total","N/A"),
                "rating": place.get("rating")
             }

        places.append(place_info)
    return places

def get_locations(location, place_type):
    list_of_places = get_places(location, place_type)
    return [
        place
        for place in list_of_places
        if place['business_status'] == 'OPERATIONAL'
        and place['rating'] is not None
        and place['user_ratings_total'] > 10
    ]

def get_directions(location, place_type):
        list_of_places = get_places(location, place_type)
        filtered_places = []
        for place in list_of_places:
            if place['business_status'] == 'OPERATIONAL' and place['rating'] is not None and place['user_ratings_total'] > 10:
                filtered_places.append(place)
                #print(filtered_places)
                visits = [(place["lat"], place["lng"]) for place in filtered_places]
                waypoints = "|".join([f"{lat},{lng}" for lat, lng in visits])
        print(filtered_places)
        directions_result = gmaps.directions(
                    origin=location,
                    destination=location,
                    waypoints=waypoints,
                    mode="walking",
                    optimize_waypoints=True
                    )
        if directions_result:
            best_route = directions_result[0]
            return best_route
        else:
            return None
    #filtiraj po ratingu,da li otvoren ili zatvoren,sta ima od tagova
    #ubaciti rating,
    #od svih lokacija koje imaju rating,izracunaj srednji i sve ispod toga izbaci
    #isto za broj user ratinga
    #print (places)
    #visits = [(place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"])
                 #for place in places]




#get_places('Novi Sad','museum')