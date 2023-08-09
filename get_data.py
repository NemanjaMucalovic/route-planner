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
    places = places_raw['results']
    #filtiraj po ratingu,da li otvoren ili zatvoren,sta ima od tagova
    #ubaciti rating,
    #od svih lokacija koje imaju rating,izracunaj srednji i sve ispod toga izbaci
    #isto za broj user ratinga
    print (places)
    visits = [(place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"])
                 for place in places]
    waypoints = "|".join([f"{lat},{lng}" for lat, lng in visits])
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



#get_places('Novi Sad','museum')