"""Contains the SQL queries for sensor retrieval"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from database import get_db
from schemas import Sensor
from status_map import normalize_status

router = APIRouter(prefix="/sensors", tags=["sensors"])

_NEIGHBORHOOD_QUERY = """
    WITH recent_readings AS (
        SELECT
            s.sensor_id,
            s.location_id,
            r.pm2_5,
            r.pm10,
            r.temperature,
            r.humidity
        FROM air_quality.sensors s
        JOIN air_quality.sensor_readings r
            ON r.sensor_id = s.sensor_id
        WHERE r.recorded_at > now() - INTERVAL '24 hours'
          AND (:include_inactive OR LOWER(s.status) = 'active')
    ),
    neighborhood_avgs AS (
        SELECT
            l.neighborhood,
            AVG(rr.pm2_5) AS pm2_5_avg,
            AVG(rr.pm10) AS pm10_avg,
            AVG(rr.temperature) AS temperature_avg,
            AVG(rr.humidity) AS humidity_avg,
            AVG(l.latitude) AS lat,
            AVG(l.longitude) AS lng,
            COUNT(DISTINCT rr.sensor_id) AS sensor_count
        FROM recent_readings rr
        JOIN air_quality.locations l
            ON l.location_id = rr.location_id
        WHERE l.neighborhood IS NOT NULL
        {neighborhood_filter}
        GROUP BY l.neighborhood
    )
    SELECT
        neighborhood,
        GREATEST(
            air_quality.pm25_aqi(pm2_5_avg),
            air_quality.pm10_aqi(pm10_avg)
        ) AS aqi,
        air_quality.aqi_category(
            GREATEST(
                air_quality.pm25_aqi(pm2_5_avg),
                air_quality.pm10_aqi(pm10_avg)
            )
        ) AS aqi_category,
        temperature_avg,
        humidity_avg,
        lat,
        lng,
        sensor_count
    FROM neighborhood_avgs
    ORDER BY neighborhood
"""


def _row_to_sensor(row: Row) -> Sensor:
    """Takes row from db and returns Sensor Object data

    Arguments:
    row SQLalchemy ROW, row of sensor information from database

    Returns:
    Sensor Class object containing sensor information
    """
    sensor_count = row.sensor_count
    return Sensor(
        id=row.neighborhood,
        name=row.neighborhood,
        type=f"{sensor_count} sensor{'s' if sensor_count != 1 else ''}",
        location=row.neighborhood,
        aqi=int(row.aqi) if row.aqi is not None else None,
        temperature=round(float(row.temperature_avg)) if row.temperature_avg is not None else None,
        humidity=round(float(row.humidity_avg)) if row.humidity_avg is not None else None,
        status=normalize_status(row.aqi_category),
        lat=float(row.lat),
        lng=float(row.lng),
    )


@router.get("", response_model=list[Sensor])
def list_sensors(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    """Lists sensors generated,

    Arguments:
    include_inactive bool : Boolean of whether to include inactive sensors
    db Session : Session information of database connection

    Returns
    list[Sensor] : list of all sensor objects

    """
    query = text(_NEIGHBORHOOD_QUERY.format(neighborhood_filter=""))
    rows = db.execute(query, {"include_inactive": include_inactive}).all()
    return [_row_to_sensor(row) for row in rows]


@router.get("/{neighborhood}", response_model=Sensor)
def get_sensor(neighborhood: str, db: Session = Depends(get_db)):
    """Gets sensor given particular neighborhood

    Arguments:
    neighborhood str : Neighborhood filter

    Returns:
    Sensor: Sensor object retrieved by filter
    """
    query = text(
        _NEIGHBORHOOD_QUERY.format(
            neighborhood_filter="AND l.neighborhood = :neighborhood"
        )
    )
    row = db.execute(
        query, {"include_inactive": True, "neighborhood": neighborhood}
    ).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Neighborhood not found")
    return _row_to_sensor(row)
