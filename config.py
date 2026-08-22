"""Loads the Cross Orgin Resource Sharing (CORS) config, for more info reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS"""
import os
from dotenv import load_dotenv

env_loaded_config = load_dotenv()
if not env_loaded_config:
    print("***NO ENVIRONMENT VARIABLE LOADED IN CONFIG, ABNORMAL RESULTS MAY FOLLOW***")


CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]
