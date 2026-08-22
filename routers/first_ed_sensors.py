"""Older version of sensors.py, DEPRECIATED"""
from typing import Optional
from warnings import warn

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from database import get_db
from schemas import Sensor
from status_map import normalize_status

router = APIRouter(prefix="/sensors", tags=["sensors"])

_SENSOR_QUERY = """
    SELECT
        s.sensor_id,
        s.name AS sensor_name,
        s.extrnl_source,
        l.neighborhood,
        l.latitude,
        l.longitude,
        aqi.aqi,
        aqi.aqi_category,
        latest.temperature,
        latest.humidity
    FROM air_quality.sensors s
    JOIN air_quality.locations l
        ON l.location_id = s.location_id
    LEFT JOIN air_quality.current_sensor_aqi aqi
        ON aqi.sensor_id = s.sensor_id
    LEFT JOIN LATERAL (
        SELECT r.temperature, r.humidity
        FROM air_quality.sensor_readings r
        WHERE r.sensor_id = s.sensor_id
        ORDER BY r.recorded_at DESC
        LIMIT 1
    ) latest ON true
    WHERE (:include_inactive OR LOWER(s.status) = 'active')
    {sensor_filter}
    ORDER BY s.name
"""


warn("Deprecated version of row-to-sensor, use sensors._row_to_sensor")
def _row_to_sensor(row: Row) -> Sensor:
    return Sensor(
        id=str(row.sensor_id),
        name=row.sensor_name,
        type=row.extrnl_source,
        location=row.neighborhood,
        aqi=int(row.aqi) if row.aqi is not None else None,
        temperature=float(row.temperature) if row.temperature is not None else None,
        humidity=float(row.humidity) if row.humidity is not None else None,
        status=normalize_status(row.aqi_category),
        lat=float(row.latitude),
        lng=float(row.longitude),
    )


warn("Deprecated version of list_sensors, use sensors.list_sensors")
@router.get("", response_model=list[Sensor])
def list_sensors(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    query = text(_SENSOR_QUERY.format(sensor_filter=""))
    rows = db.execute(query, {"include_inactive": include_inactive}).all()
    return [_row_to_sensor(row) for row in rows]


warn("Deprecated version of get_sensor, use sensors.get_sensor")
@router.get("/{sensor_id}", response_model=Sensor)
def get_sensor(sensor_id: str, db: Session = Depends(get_db)):
    """Returns a single sensor by id, regarless of status."""
    query = text(
        _SENSOR_QUERY.format(sensor_filter="AND s.sensor_id::text = :sensor_id")
    )
    row = db.execute(
        query, {"include_inactive": True, "sensor_id": sensor_id}
    ).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return _row_to_sensor(row)
