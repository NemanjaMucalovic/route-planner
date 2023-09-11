import uuid
from typing import List, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class Direction(BaseModel):
    location: str
    place_type: str
    date: str


class PlacesInput(BaseModel):
    location: str
    place_type: str
    date: str


class ResponseDirection(BaseModel):
    locations: List
    directions: Dict
    csv_id: str
    set_id: str


class PlacesID(BaseModel):
    id: str


class PlacesSet(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    start_location: str
    date: datetime
    locations: List


class DirectionSet(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    overview_polyline: str
    location_reference: str = Field(
        default_factory=uuid.uuid4, alias="_location_reference"
    )


class APICallStats(BaseModel):
    timestamp: datetime
    function: str
