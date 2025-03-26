import os
from datetime import date
from decimal import Decimal
import requests

# OXR API
OXR_APP_ID = os.environ.get("OXR_APP_ID")
URL_LATEST = 'http://openexchangerates.org/api/latest.json'
URL_HISTORICAL = 'http://openexchangerates.org/api/historical/{0}.json'


def get_exchange_rate_latest(base_currency: str, target_currency: str, api_key=OXR_APP_ID):
    """
    Fetches the latest exchange rate between two currencies.
    """
    url = f"{URL_LATEST}?app_id={api_key}&base={base_currency}&symbols={target_currency}"

    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    rate = Decimal(str(data['rates'][target_currency]))
    return rate


def get_exchange_rate_historical(base_currency: str, target_currency: str, d: date | str, api_key=OXR_APP_ID):
    """
    Fetches the exchange rate for a specific date.
    """
    url = f"{URL_HISTORICAL.format(d)}?app_id={api_key}&base={base_currency}&symbols={target_currency}"

    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    rate = Decimal(str(data['rates'][target_currency]))
    return rate
