from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import datetime
from generate_data import generate_directions
from fastapi.middleware.cors import CORSMiddleware
from database import get_data, insert_data
from helpers import write_data_to_csv
from models import Direction, ResponseDirection, LocationSet


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "alive"}


@app.post("/directions", status_code=201, response_model=ResponseDirection)
async def post_data(direction: Direction):
    """
    Generate directions for specified location and place type on a given date.

    This endpoint takes a Direction object as input and generates directions for a specified
    location and place type on the provided date. It first validates the date to ensure it's
    not in the past. Then, it generates directions and related data using the provided input
    parameters and inserts the data into the appropriate collections in the database. Finally,
    it returns a ResponseDirection object containing the generated locations, directions,
    CSV file ID, and set ID from the database.
    """

    current_date = datetime.date.today()
    received_date = datetime.datetime.strptime(direction.date, "%Y-%m-%d").date()
    if received_date < current_date:
        raise HTTPException(status_code=400, detail="wrong date received")
    data = generate_directions(
        location=direction.location,
        place_type=direction.place_type,
        date=direction.date,
    )
    locations_set_id = insert_data(data[2], collection="locations")
    csv_id = write_data_to_csv(data[0])
    return ResponseDirection(
        locations=data[0], directions=data[1], csv_id=csv_id, set_id=locations_set_id
    )


@app.get("/locations/{set_id}", response_model=LocationSet)
async def get_single_location_data(set_id: str):
    """
    Retrieve location data from the database for a specific set ID.

    This endpoint retrieves location data from the database for a specific set ID. The set ID
    is used to identify a specific collection in the database containing location information.
    The retrieved data includes the ID, start location, and a list of locations associated with
    the set. The data is returned in the form of a LocationSet object.
    """
    data = get_data(set_id, collection="locations")
    if not data:
        raise HTTPException(status_code=404, detail="set not found")
    else:
        return LocationSet(
        id=data["id"],
        start_location=data["start_location"],
        locations=data["locations"],
        )


@app.get("/downloads/{csv_id}", response_class=FileResponse)
async def get_csv(csv_id: str):
    """
    Download a CSV file by its ID.

    This endpoint allows users to download a CSV file based on the provided CSV ID.
    It first checks if the specified CSV file exists in the 'csv' directory. If the file
    is found, it returns the file for download using the FileResponse class. If the file
    is not found, a 404 Not Found response is raised.
    """
    if not os.path.isfile(f"csv/{csv_id}.csv"):
        raise HTTPException(status_code=404, detail="file not found")
    else:
        return f"csv/{csv_id}.csv"
