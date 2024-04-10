from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src import currency_parser, exchange_rate


def test_split_currency_amount_code():
    assert currency_parser.split_currency_amount_code("100EUR") == (100, "EUR")
    assert currency_parser.split_currency_amount_code("350USD") == (350, "USD")
    assert currency_parser.split_currency_amount_code("1000BRL") == (1000, "BRL")


def test_split_currency_string():
    result = currency_parser.parse_currency_string("100EUR + 350USD + 1000BRL")
    assert result == [(100, "EUR"), (350, "USD"), (1000, "BRL")]

    # Test with spaces and different order
    result = currency_parser.parse_currency_string(" 100EUR +1000BRL+  350USD")
    assert result == [(100, "EUR"), (1000, "BRL"), (350, "USD")]

    # Test with invalid input
    with pytest.raises(ValueError):
        currency_parser.parse_currency_string("100EUR + invalid + 350USD")

    # Test without currency
    with pytest.raises(ValueError):
        currency_parser.parse_currency_string("999")

    # Test without amount
    with pytest.raises(ValueError):
        currency_parser.parse_currency_string("BRL")


@patch("src.currency_parser.convert_to")
def test_run_exchange_valid(mocked_convert_to):
    mocked_convert_to.return_value = 10

    currency_string = "10USD + 20EUR + 300BRL to GBP"
    expected_result = 30  # 10$ for each time convert_to is called (3x)
    assert currency_parser.run_exchange(currency_string) == expected_result


def test_convert_to():
    mock_currency_rates = MagicMock()
    mock_currency_rates.get_rate.return_value = 1.5
    with patch("src.exchange_rate.CurrencyRates", return_value=mock_currency_rates):
        amount = 100
        from_currency = "USD"
        to_currency = "EUR"
        when = datetime.now()

        converted_amount = exchange_rate.convert_to(
            amount, from_currency, to_currency, when
        )

        mock_currency_rates.get_rate.assert_called_once_with(
            from_currency, to_currency, when
        )

        assert converted_amount == amount * mock_currency_rates.get_rate.return_value


def test_run_exchange_invalid_string():
    invalid_currency_string = "10USD"  # Missing currency to convert to
    with pytest.raises(Exception):
        currency_parser.run_exchange(invalid_currency_string)


def test_run_exchange_invalid_amount():
    invalid_currency_string = "USD + EUR to GBP"
    with pytest.raises(ValueError):
        currency_parser.run_exchange(invalid_currency_string)


def test_run_exchange_invalid_symbol():
    invalid_currency_string = "100PPP to WWW"
    with pytest.raises(Exception):
        currency_parser.run_exchange(invalid_currency_string)
