
"""Maps && returns normalized value of status of sensor"""

_STATUS_MAP = {
    "good": "good",
    "moderate": "moderate",
    "unhealthy for sensitive groups": "sensitive",
    "unhealthy": "unhealthy",
    "very unhealthy": "veryunhealthy",
    "hazardous": "hazardous",
}


def normalize_status(aqi_category: str | None) -> str:
    """Sets default to 'unknown' if aqi_category is None

    Keyword arguments:
    aqi_category -- The generated AQI value using, the status map

    Returns:
    string containing aqi category (defaults to unknown)
    """
    if not aqi_category:
        return "unknown"
    return _STATUS_MAP.get(aqi_category.strip().lower(), "unknown")
