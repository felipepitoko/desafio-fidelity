import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
API_URL = os.getenv("API_URL", "http://localhost:8000") # Default for local dev, overridden by docker-compose
PROCESS_INTERVAL_SECONDS = int(os.getenv("PROCESS_INTERVAL_SECONDS", 60))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 5))