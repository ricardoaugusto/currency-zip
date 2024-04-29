import re
from datetime import datetime


def split_currency_amount_code(currency_string):
    """
    Split currency string into two parts: amount and code
    :param currency_string:
    :return:
    """
    match = re.match(r"(\d+(?:[.,]\d+)?)(\D+)", currency_string)
    if match:
        return float(match.group(1).replace(",", ".")), match.group(2)
    else:
        raise ValueError("Invalid currency string")


def parse_currency_string(currency_string):
    """
    Returns a tupled list of (amount,code) currencies

    :param currency_string:
    :return:
    """
    currency_list = [
        split_currency_amount_code(part.strip()) for part in currency_string.split("+")
    ]
    return currency_list


def parse_date(date_str):
    """
    Converts a date string in YYYYMMDD format to a
    tuple of year, month, day

    :param date_str: The date string to parse
    :return: A tuple representing the parsed date in year, month, day
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y%m%d").date()

        year = date_obj.year
        month = date_obj.month
        day = date_obj.day

        return year, month, day
    except ValueError:
        print("Invalid date format. Please provide the date in YYYYMMDD format.")
        return None
