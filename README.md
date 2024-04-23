# currency-zip

![version](https://img.shields.io/badge/version-v0.2.0-white) ![pytest](https://img.shields.io/badge/coverage-100%25-green) ![forks](https://img.shields.io/github/forks/ricardoaugusto/currency-zip
)

# Purpose

To make banking/invoicing easier. Add currency conversion between multiple income sources and aggregate the total into a single currency.

# Installation

Clone the repository and create a Python venv:

```shell
git clone git@github.com:ricardoaugusto/currency-zip.git
cd currency-zip
python3 -m venv .venv
source .venv/bin/activate
```

_On Windows, change to `python -m venv .venv` and `source .venv\Scripts\activate`._

Check if your .venv is set:

```shell
which python
/Users/ricardoaugusto/dev/currency-zip/.venv/bin/python
```

Install the `requirements.txt`:

```shell
pip install -r requirements.txt
```

Finally, create a free account at http://freecurrencyapi.com and update the `src/.env` with your apiKey.

# Usage

```shell
python czip.py "100EUR + 250USD + 1000BRL to GBP"
438.46GBP on 20240415
```

To get the exchange rate for a specific date, use `--when=YYYYMMDD`:
```shell
python czip.py "100EUR + 250USD + 1000BRL to GBP" --when=20240101
445.61GBP on 20240101
```

# Testing

```shell
pytest --cov=src tests --cov-report=html:tests/coverage
===== test session starts ======
platform darwin -- Python 3.11.4, pytest-8.1.1, pluggy-1.4.0
rootdir: /Users/ricardoaugusto/dev/currency-zip
plugins: cov-5.0.0
collected 13 items

tests/unit_test.py ...........                                  [100%]

---------- coverage: platform darwin, python 3.11.4-final-0 ----------
Coverage HTML written to dir tests/coverage

===== 13 passed in 0.29s ======
```

# Contributing