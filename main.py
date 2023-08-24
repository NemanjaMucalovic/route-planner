from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import datetime
from get_data import get_directions
from fastapi.middleware.cors import CORSMiddleware


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

@app.post("/direction")
async def post_data(direction: Direction):
    current_date = datetime.date.today()
    received_date = datetime.datetime.strptime(direction.date, "%Y-%m-%d").date()
    if received_date < current_date:
        raise HTTPException(status_code=400, detail="wrong date received")
    else:
        return get_directions(location=direction.location, place_type=direction.place_type, date=direction.date)

@app.get("/downloads/{csv_id}", response_class=FileResponse)
async def get_csv(csv_id: str):
    if not os.path.isfile(f'{csv_id}.csv'):
        raise HTTPException(status_code=404, detail="file not found")
    else:
        return f'{csv_id}.csv'




