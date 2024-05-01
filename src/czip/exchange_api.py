import os

import requests
from dotenv import dotenv_values

script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, ".env")

env = dotenv_values(env_path)
api_key = env.get("API_KEY")
currencies = env.get("CURRENCIES")


def run_exchange(
    amount,
    from_currency,
    to_currency,
    year=None,
    month=None,
    day=None,
    historical=False,
):
    try:
        endpoint = "historical" if historical else "latest"

        exchange_url = f"https://api.freecurrencyapi.com/v1/{endpoint}?apikey={api_key}&base_currency={from_currency}&currencies={currencies}"
        if historical:
            exchange_url += f"&date={year}-{month}-{day}"

        response = requests.get(exchange_url)
        response.raise_for_status()
        data = response.json()

        if historical is True:
            key = "{:04d}-{:02d}-{:02d}".format(year, month, day)
            to_currency_rate = data.get("data", {}).get(key, {}).get(to_currency)
        else:
            to_currency_rate = data.get("data", {}).get(to_currency)

        converted_amount = amount * to_currency_rate
        return round(converted_amount, 2)

    except Exception as e:
        print(f"Error during conversion: {e}")
        return 0.0
