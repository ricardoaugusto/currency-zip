from datetime import datetime, timedelta

from src.czip.exceptions.missing_currency_exception import MissingCurrencyException
from src.czip.exchange_api import run_exchange
from src.czip.string_parser import parse_currency_string, parse_date


def convert(currency_string, when=None):
    """
    Runs the exchange by splitting the given input string
    into a list of tuples containing the (amount, code),
    sum the exchanged values for the given currency.

    :param currency_string: The currency string to parse.
    :param when: Optional. The date to use for exchange rates.
                 Defaults to datetime.now().date() if not provided.
                 Can be a string in YYYYMMDD format or a datetime object.
    :return: The result of the exchange.
    """
    historical = True
    if when is None or not isinstance(when, str):
        current_datetime = datetime.now()
        one_hour_ago = current_datetime - timedelta(days=1)
        when = one_hour_ago.date().strftime("%Y%m%d")
        historical = False

    year, month, day = parse_date(when)

    # If no currency to convert to was given
    split_currency_string = currency_string.split(" to ")
    if len(split_currency_string) != 2:
        raise MissingCurrencyException()

    # Finally gets the exchange rate and sums everything
    result = 0
    to_currency = split_currency_string[1]
    currencies = parse_currency_string(split_currency_string[0])
    if currencies:
        for amount, from_currency in currencies:
            result += run_exchange(
                amount, from_currency, to_currency, year, month, day, historical
            )

    return f"{result}{to_currency} on {when}"
