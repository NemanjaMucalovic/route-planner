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
        print(best_route)
        print("Best Route Summary:")
        print("Start Location:", best_route['legs'][0]['start_address'])
        print("End Location:", best_route['legs'][0]['end_address'])
        print("Total Distance:", best_route['legs'][0]['distance']['text'])
        print("Total Duration:", best_route['legs'][0]['duration']['text'])
        print("Waypoints (in order):")
        for waypoint in best_route['waypoint_order']:
            print(places[waypoint]["name"])
    else:
        return None



get_places('Novi Sad','museum')