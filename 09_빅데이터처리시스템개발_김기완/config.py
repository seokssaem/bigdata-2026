import os

AIRPORT_DB_URL = os.getenv(
    'AIRPORT_DB_URL',
    'postgresql://postgres:1234@localhost:5432/airportdb',
)

CONGESTION_THRESHOLD = 2.0