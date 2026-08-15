from typing import Optional

from pydantic import BaseModel


class Sensor(BaseModel):
    id: str
    name: str
    type: Optional[str] = None
    location: Optional[str] = None
    aqi: Optional[int] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    status: str = "unknown"
    lat: float
    lng: float

    class Config:
        from_attributes = True
