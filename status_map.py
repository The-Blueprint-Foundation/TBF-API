
_STATUS_MAP = {
    "good": "good",
    "moderate": "moderate",
    "unhealthy for sensitive groups": "sensitive",
    "unhealthy": "unhealthy",
    "very unhealthy": "veryunhealthy",
    "hazardous": "hazardous",
}


def normalize_status(aqi_category: str | None) -> str:
    if not aqi_category:
        return "unknown"
    return _STATUS_MAP.get(aqi_category.strip().lower(), "unknown")
