from helpers import check_workhours


def sort_places_by_ratings(list_of_places):
    return [
        place
        for place in list_of_places
        if place["business_status"] == "OPERATIONAL"
        and place["rating"] is not None
        and place["user_ratings_total"] > 10
    ]


def sort_places_by_working_hours(list_of_places, date):
    return [
        place
        for place in list_of_places
        if check_workhours(place.get("place_id"), date)
    ]


def sort_places_by_is_opened_status(list_of_places):
    return [place for place in list_of_places if place["is_opened"] is True]


def create_waypoints(list_of_places):
    visits = [(place["lat"], place["lng"]) for place in list_of_places]
    return "|".join([f"{lat},{lng}" for lat, lng in visits])
