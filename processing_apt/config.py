import os
DB_URL = os.getenv(
    'DB_URL',
    'postgresql://postgres:1234@localhost:5432/aptapidb'
)