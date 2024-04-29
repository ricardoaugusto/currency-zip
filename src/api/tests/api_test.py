from fastapi.testclient import TestClient
from src.api.api import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text.strip('"') == "Welcome to CZip! Send a POST to /convert"


def test_convert_currency():
    data = {"currency": "100USD to EUR"}
    response = client.post("/convert", json=data)
    assert response.status_code == 200
    assert "result" in response.json()
    assert "EUR" in response.text


def test_convert_currency_when():
    data = {"currency": "100USD to EUR", "when": "20240101"}
    response = client.post("/convert", json=data)
    assert response.status_code == 200
    assert "result" in response.json()
    assert "20240101" in response.text


def test_convert_currency_but_missing_currency():
    data = {"when": "20240101"}
    response = client.post("/convert", json=data)
    assert response.status_code == 422


def test_convert_currency_invalid_when():
    data = {"currency": "1000USD to EUR", "when": "tomorrow"}
    response = client.post("/convert", json=data)
    assert response.status_code == 500
