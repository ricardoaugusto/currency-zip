import pytest


@pytest.fixture
def basic_mock_response():
    return {"data": {"USD": 1.0, "EUR": 0.85, "GBP": 0.73, "BRL": 5.27}}


@pytest.fixture
def historical_mock_response():
    return {"data": {"2024-04-22": {"USD": 1.0, "EUR": 0.85, "GBP": 0.73, "BRL": 5.27}}}
