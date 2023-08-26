from helpers import check_workhours

def sort_places_by_ratings(list_of_places):
    return [
        place
        for place in list_of_places
        if place['business_status'] == 'OPERATIONAL'
        and place['rating'] is not None
        and place['user_ratings_total'] > 10
    ]

def sort_places_by_working_hours(list_of_places, date):
    return [
        place for place in list_of_places if check_workhours(place.get('place_id'), date)
    ]