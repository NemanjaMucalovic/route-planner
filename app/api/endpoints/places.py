import os
import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from app.services.google_maps import GoogleMapsAPI
from app.db.models import PlacesID, PlacesInput, PlacesSet
from app.db.crud import insert_data, get_data
from app.utils.utils import verify_date


google_maps_api = GoogleMapsAPI(api_key=os.environ.get("GOOGLE_MAPS_API_KEY"))

router = APIRouter()


@router.post("/places", status_code=201, response_model=PlacesID)
async def post_places(places: PlacesInput):
    if verify_date(places.date) is not True:
        raise HTTPException(status_code=400, detail="wrong format/date received")
    data = google_maps_api.generate_filtered_places(
        location=places.location,
        place_type=places.place_type,
        date=places.date,
        disable_workhours=True,
    )
    if len(data) == 0:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "there were no places"}
        )
    # TODO move to models class
    locations_data_set = {
        "date": datetime.datetime.now(),
        "start_location": places.location,
        "locations": data,
    }
    data_id = insert_data(locations_data_set, "places")
    print(data_id)
    return PlacesID(id=data_id)


@router.get("/places/{set_id}", response_model=PlacesSet)
async def get_place(set_id: str):
    data = get_data(data_id=set_id, collection="places")
    if not data:
        raise HTTPException(status_code=404, detail="set not found")
    return PlacesSet(
        start_location=data["start_location"],
        date=data["date"],
        locations=data["locations"],
    )
