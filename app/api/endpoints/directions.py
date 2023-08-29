from fastapi import APIRouter, HTTPException
import os
from bson.objectid import ObjectId
from app.services.google_maps import GoogleMapsAPI
from app.db.models import PlacesID, PlacesInput, PlacesSet, DirectionSet
from app.db.crud import insert_data, get_data

google_maps_api = GoogleMapsAPI(api_key=os.environ.get('GOOGLE_MAPS_API_KEY'))

router = APIRouter()

@router.get("/directions/{set_id}")
async def get_directions(set_id: str):
    data = get_data(data_id=set_id, collection="places")
    if not data:
        raise HTTPException(status_code=404, detail="set not found")
    new_list = data["locations"]
    waypoints = google_maps_api.create_waypoints(new_list)
    directions = google_maps_api.get_directions(location=data["start_location"],waypoints=waypoints)
    #TODO: move to model class
    data_set = {"overview_polyline":directions["overview_polyline"]["points"],
                "location_reference": ObjectId(set_id)}
    insert_data(data_set,collection="directions")
    return directions

