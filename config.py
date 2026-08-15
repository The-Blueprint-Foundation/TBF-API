import os
 
from dotenv import load_dotenv

load_dotenv()
 
CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]
