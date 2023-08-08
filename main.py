from fastapi import FastAPI
from pydantic import BaseModel
from get_data import get_places
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Direction(BaseModel):
    place_type: str

@app.get("/health")
def health_check():
    return {"status": "alive"}


@app.post("/direction")
def post_data(direction: Direction):
    return get_places(location='Novi Sad', place_type=direction.place_type)


