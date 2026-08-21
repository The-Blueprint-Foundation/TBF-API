"""Main API calling, acts as 'index' for API"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ORIGINS
from routers.sensors import router as sensors_router

app = FastAPI(title="The Blueprint Foundation - Change is in the Air API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(sensors_router)


@app.get("/health")
def health()->dict[str,str]:
    """ Gets 'health' status of the sensor, whether sensor is operational

    Returns dict[str,str] status of sensor, defaulted to 'ok'"""
    return {"status": "ok"}


@app.get("/")
def root()->dict[str,str]:
    """Acts as 'root' of the index, when no other call specified

    Returns dict[str,str] : standard string for 'root' of the API, acts as connection check"""
    return {"message": "Hello from FastAPI on Google Cloud!"}

