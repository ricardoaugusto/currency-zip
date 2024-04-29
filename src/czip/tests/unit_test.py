from unittest.mock import patch

import pytest

from src.czip.tests.fixtures import basic_mock_response, historical_mock_response
import src
from src.czip import currency_conversion, exchange_api, string_parser


def test_basic_conversion(basic_mock_response):
    with patch("src.czip.exchange_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = basic_mock_response

        amount = 100
        from_currency = "USD"
        to_currency = "EUR"
        result = exchange_api.run_exchange(amount, from_currency, to_currency)

        assert result == 85.0


def test_historical_conversion(historical_mock_response):
    with patch("src.czip.exchange_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = historical_mock_response

        amount = 100
        from_currency = "USD"
        to_currency = "EUR"
        year = 2024
        month = 4
        day = 22
        result = exchange_api.run_exchange(
            amount,
            from_currency,
            to_currency,
            year=year,
            month=month,
            day=day,
            historical=True,
        )

        assert result == 85.0


def test_basic_conversion_with_decimal_currency(basic_mock_response):
    with patch("src.czip.exchange_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = basic_mock_response

        amount = 9999.90
        from_currency = "USD"
        to_currency = "EUR"
        result = exchange_api.run_exchange(amount, from_currency, to_currency)

        assert result == 8499.91


def test_currency_conversion_with_invalid_json():
    with patch("src.czip.exchange_api.requests.get") as mock_get:
        mock_response = "invalid json"
        mock_get.return_value.json.return_value = mock_response

        amount = 100
        from_currency = "USD"
        to_currency = "EUR"
        result = exchange_api.run_exchange(amount, from_currency, to_currency)

        assert result == 0.0


def test_split_currency_amount_code():
    assert src.czip.string_parser.split_currency_amount_code("100EUR") == (100, "EUR")
    assert src.czip.string_parser.split_currency_amount_code("350USD") == (350, "USD")
    assert src.czip.string_parser.split_currency_amount_code("1000BRL") == (
        1000,
        "BRL",
    )


def test_split_decimal_currency_amount_code():
    assert src.czip.string_parser.split_currency_amount_code("100.90EUR") == (
        100.9,
        "EUR",
    )
    assert src.czip.string_parser.split_currency_amount_code("350.90USD") == (
        350.9,
        "USD",
    )
    assert src.czip.string_parser.split_currency_amount_code("1000,95BRL") == (
        1000.95,
        "BRL",
    )


def test_split_currency_string():
    result = src.czip.string_parser.parse_currency_string("100EUR + 350USD + 1000BRL")
    assert result == [(100, "EUR"), (350, "USD"), (1000, "BRL")]

    # Test with spaces and different order
    result = src.czip.string_parser.parse_currency_string(" 100EUR +1000BRL+  350USD")
    assert result == [(100, "EUR"), (1000, "BRL"), (350, "USD")]

    # Test with invalid input
    with pytest.raises(ValueError):
        src.czip.string_parser.parse_currency_string("100EUR + invalid + 350USD")

    # Test without currency
    with pytest.raises(ValueError):
        src.czip.string_parser.parse_currency_string("999")

    # Test without amount
    with pytest.raises(ValueError):
        src.czip.string_parser.parse_currency_string("BRL")


@patch("src.czip.exchange_api.run_exchange")
@patch("src.czip.exchange_api.requests.get")
def test_currency_conversion_valid(mocked_run_exchange, mocked_get):
    mocked_get.return_value = 1.0
    mocked_run_exchange.return_value = 10

    currency_string = "10USD + 20EUR + 300BRL to GBP"
    expected_result = "0.0GBP on 20240101"
    assert currency_conversion.convert(currency_string, "20240101") == expected_result


@patch("src.czip.exchange_api.run_exchange")
@patch("src.czip.exchange_api.requests.get")
def test_currency_conversion_valid_when(mocked_run_exchange, mocked_get):
    mocked_get.return_value = 1.0
    mocked_run_exchange.return_value = 10

    currency_string = "10USD + 20EUR + 300BRL to GBP"
    when = "20240101"
    expected_result = "0.0GBP on 20240101"
    assert currency_conversion.convert(currency_string, when) == expected_result


def test_currency_conversion_invalid_when():
    when = "12345"  # Not a valid YYYYMMDD date
    result = src.czip.string_parser.parse_date(when)

    assert result is None


def test_currency_conversion_invalid_string():
    invalid_currency_string = "10USD"  # Missing currency to convert to
    with pytest.raises(Exception):
        currency_conversion.convert(invalid_currency_string)


def test_currency_conversion_invalid_amount():
    invalid_currency_string = "USD + EUR to GBP"  # Missing value
    with pytest.raises(ValueError):
        currency_conversion.convert(invalid_currency_string)


def test_currency_conversion_invalid_symbol():
    invalid_currency_string = "100PPP to WWW"  # Currency not supported
    result = currency_conversion.convert(invalid_currency_string, "20240101")
    assert result == "0.0WWW on 20240101"
