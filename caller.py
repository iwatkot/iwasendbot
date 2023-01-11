import requests

from decouple import config

API_URL = "https://api.short.io/links"
DOMAIN = config('DOMAIN')
API_KEY = config('API_KEY')
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": API_KEY
}


def short_url(long_url):
    payload = {
        "domain": DOMAIN,
        "originalURL": long_url,
    }
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    return response.json()['shortURL']
