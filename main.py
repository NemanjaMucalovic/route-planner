import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.utils.utils import create_directory
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    directory_path = "storage"  # Specify the directory path you want to create
    create_directory(directory_path)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "alive"}


app.include_router(api_router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9009, reload=True)
