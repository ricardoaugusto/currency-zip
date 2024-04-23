from unittest.mock import patch

import pytest

import src.string_parser
from src import currency_conversion, exchange_api, localization


def test_basic_conversion():
    with patch("src.exchange_api.requests.get") as mock_get:
        mock_response = {"data": {"USD": 1.0, "EUR": 0.85, "GBP": 0.73, "BRL": 5.27}}
        mock_get.return_value.json.return_value = mock_response

        amount = 100
        from_currency = "USD"
        to_currency = "EUR"
        result = exchange_api.run_exchange(amount, from_currency, to_currency)

        assert result == 85.0


def test_historical_conversion():
    with patch("src.exchange_api.requests.get") as mock_get:
        mock_response = {
            "data": {"2024-04-22": {"USD": 1.0, "EUR": 0.85, "GBP": 0.73, "BRL": 5.27}}
        }
        mock_get.return_value.json.return_value = mock_response

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


def test_currency_conversion_with_invalid_json():
    with patch("src.exchange_api.requests.get") as mock_get:
        mock_response = "invalid json"
        mock_get.return_value.json.return_value = mock_response

        amount = 100
        from_currency = "USD"
        to_currency = "EUR"
        result = exchange_api.run_exchange(amount, from_currency, to_currency)

        assert result == 0.0


def test_split_currency_amount_code():
    assert src.string_parser.split_currency_amount_code("100EUR") == (100, "EUR")
    assert src.string_parser.split_currency_amount_code("350USD") == (350, "USD")
    assert src.string_parser.split_currency_amount_code("1000BRL") == (
        1000,
        "BRL",
    )


def test_split_currency_string():
    result = src.string_parser.parse_currency_string("100EUR + 350USD + 1000BRL")
    assert result == [(100, "EUR"), (350, "USD"), (1000, "BRL")]

    # Test with spaces and different order
    result = src.string_parser.parse_currency_string(" 100EUR +1000BRL+  350USD")
    assert result == [(100, "EUR"), (1000, "BRL"), (350, "USD")]

    # Test with invalid input
    with pytest.raises(ValueError):
        src.string_parser.parse_currency_string("100EUR + invalid + 350USD")

    # Test without currency
    with pytest.raises(ValueError):
        src.string_parser.parse_currency_string("999")

    # Test without amount
    with pytest.raises(ValueError):
        src.string_parser.parse_currency_string("BRL")


@patch("src.exchange_api.run_exchange")
@patch("src.exchange_api.requests.get")
def test_currency_conversion_valid(mocked_run_exchange, mocked_get):
    mocked_get.return_value = 1.0
    mocked_run_exchange.return_value = 10

    currency_string = "10USD + 20EUR + 300BRL to GBP"
    expected_result = "0.0GBP on 20240101"
    assert currency_conversion.convert(currency_string, "20240101") == expected_result


@patch("src.exchange_api.run_exchange")
@patch("src.exchange_api.requests.get")
def test_currency_conversion_valid_when(mocked_run_exchange, mocked_get):
    mocked_get.return_value = 1.0
    mocked_run_exchange.return_value = 10

    currency_string = "10USD + 20EUR + 300BRL to GBP"
    when = "20240101"
    expected_result = "0.0GBP on 20240101"
    assert currency_conversion.convert(currency_string, when) == expected_result


def test_currency_conversion_invalid_when():
    when = "12345"  # Not a valid YYYYMMDD date
    result = src.string_parser.parse_date(when)

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


def test_delocalize_currency():
    result = localization.delocalize_currency("100,50", "EUR")
    assert result == 100.5

    result = localization.delocalize_currency("100,500.90", "USD")
    assert result == 100500.90

    result = localization.delocalize_currency("100,000.50", "GBP")
    assert result == 100000.5

    result = localization.delocalize_currency("100.000,05", "BRL")
    assert result == 100000.05


def test_delocalize_currency_wrong_input():
    result = localization.delocalize_currency("100.500,00", "USD")
    assert result == 100.5
