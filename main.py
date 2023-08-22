from fastapi import FastAPI,Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from get_data import get_places, get_directions
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
    return get_directions(location=direction.location, place_type=direction.place_type, date=direction.date)

@app.get("/downloads/{csv_id}", response_class=FileResponse)
async def get_csv(csv_id: str):
    return f'{csv_id}.csv'




