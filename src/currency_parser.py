import re
from datetime import datetime

from src.exceptions.missing_currency_exception import MissingCurrencyException
from src.exchange_rate import convert_to
from src.localization import delocalize_currency


def split_currency_amount_code(currency_string):
    """
    Split currency string into two parts: amount and code
    :param currency_string:
    :return:
    """
    match = re.match(r"(\d+)(\D+)", currency_string)
    if match:
        return delocalize_currency(match.group(1), match.group(2)), match.group(2)
    else:
        raise ValueError("Invalid currency string")


def parse_currency_string(currency_string):
    """
    Returns a tupled list of (amount,code) currencies

    :param currency_string:
    :return:
    """
    currency_list = [
        (int(amount), code)
        for amount, code in (
            split_currency_amount_code(part.strip())
            for part in currency_string.split("+")
        )
    ]
    return currency_list


def parse_date(date_str):
    """
    Converts a date string in YYYYMMDD format to a
    datetime object

    :param date_str: The date string to parse
    :return: A datetime object representing the parsed date
    """
    try:
        return datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        print("Invalid date format. Please provide the date in YYYYMMDD format.")
        return None


def run_exchange(currency_string, when=None):
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
    if when is None:
        when = datetime.now().date()
    elif isinstance(when, str):
        when = parse_date(when)

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
            result += convert_to(amount, from_currency, to_currency, when)

    return f"{result}{to_currency} on {when}"
