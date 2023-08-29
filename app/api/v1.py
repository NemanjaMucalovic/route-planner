from fastapi import APIRouter
from app.api.endpoints import directions, places, pdf

api_router = APIRouter()

# Include existing routers under the /v1 prefix
api_router.include_router(directions.router, tags=["directions"])
api_router.include_router(places.router, tags=["places"])
api_router.include_router(pdf.router, tags=["pdf"])
