import os

LOTTERAPI_DB_URL = os.getenv(
    'LOTTERAPI_DB_URL',
    'postgresql://postgres:1234@localhost:5432/lotteryaipdb'
)

lottery_win_min = 2
lottery_win_max = 3

lottery_address = {'대구'}