from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import datetime
from generate_data import generate_directions
from fastapi.middleware.cors import CORSMiddleware
from database import get_data, insert_data
from helpers import write_data_to_csv



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Direction(BaseModel):
    location: str
    place_type: str
    date: str


@app.get("/health")
async def health_check():
    return {"status": "alive"}

@app.post("/directions")
async def post_data(direction: Direction):
    #ubaciti check za datum u neku posebnu funkciju
    current_date = datetime.date.today()
    received_date = datetime.datetime.strptime(direction.date, "%Y-%m-%d").date()
    if received_date < current_date:
        raise HTTPException(status_code=400, detail="wrong date received")
    else:
        data = generate_directions(location=direction.location, place_type=direction.place_type, date=direction.date)
        locations_set_id = insert_data(data[2], collection="locations")
        name_of_csv = {"csv_id": write_data_to_csv(data[0])}
        return [data[0], data[1], name_of_csv, {"locations_set_id":locations_set_id}]

@app.get("/locations/{set_id}")
async def get_single_location_data(set_id: str):
    return get_data(set_id,collection="locations")


@app.get("/downloads/{csv_id}", response_class=FileResponse)
async def get_csv(csv_id: str):
    if not os.path.isfile(f'csv/{csv_id}.csv'):
        raise HTTPException(status_code=404, detail="file not found")
    else:
        return f'csv/{csv_id}.csv'




