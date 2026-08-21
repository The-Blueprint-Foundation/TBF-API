"""Schema containing the sensor class for later use"""

from pydantic import BaseModel

class Sensor(BaseModel):
    """Sensor Class to hold all information

    Attributes:

    ID          -- ID number of sensor as a string \n
    Name        -- Name of sensor, random string \n
    type        -- Type of the sensor (synthetic or QuantAQ or Bottlebot), as a string \n
    location    -- Location of sensor, a neighborhood in portland / gresham, as a string \
    aqi         -- Air Quality Index Number, as a float \n
    temperature -- Temperature, in Fahrenheit as a float \n
    humidity    -- Humidity, in percentage as a float \n
    status      -- 'Status' of the sensor, most often just good, as a string (default unknown) \n
    lat         -- Latitude value of the sensor, as a float \n
    lng         -- Longitude value of the sensor, as a float \n

    Sub-Class:

    config      -- Acts as a pydantic config class, need just for attributes
    
    """    
    id: str
    name: str
    type: str | None = None
    location: str | None = None
    aqi: int | None = None
    temperature: float | None = None
    humidity: float | None = None
    status: str = "unknown"
    lat: float
    lng: float

    class Config:
        from_attributes = True
