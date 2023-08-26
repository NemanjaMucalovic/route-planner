from typing import List, Dict
from pydantic import BaseModel


class Direction(BaseModel):
    location: str
    place_type: str
    date: str


class ResponseDirection(BaseModel):
    locations: List
    directions: Dict
    csv_id: str
    set_id: str


class LocationSet(BaseModel):
    id: str
    start_location: str
    locations: List
