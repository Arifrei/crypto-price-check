import requests as rq
from dotenv import load_dotenv
import os

load_dotenv()
ep = "https://api.coingecko.com/api/v3/coins/markets"

headers = {
        "x-cg-demo-api-key": os.getenv('API_KEY'),
    }
params = {
    "ids": "bitcoin",
    "vs_currency": "usd",
}
response = rq.get(ep, headers=headers, params=params)
print(response.json())