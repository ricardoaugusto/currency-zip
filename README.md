# currency-zip

![version](https://img.shields.io/badge/version-v0.4.2-white) ![pytest](https://img.shields.io/badge/coverage-100%25-green) ![forks](https://img.shields.io/github/forks/ricardoaugusto/currency-zip
)

# Purpose

To make banking/invoicing easier. Add currency conversion between multiple income sources and aggregate the total into a single currency.

# Installation

Steps:
1. Clone this repo
2. Create and activate the .venv
3. Install the requirements
4. Get an API_KEY
5. Optional: install the czip.sh executable

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


Create a free account at http://freecurrencyapi.com and update the `src/.env` with your API_KEY.

Finally, to make the responses shorter and faster, enable in the `src/.env` only the currencies you'll be using.

A full list of currencies is available at https://api.freecurrencyapi.com/v1/currencies.

## Optional

Terminal usage with `sh czip.sh`.

Run `sudo sh install.sh` to use it as executable.

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

If you installed `czip` as executable with `install.sh` then you can run it interactively:

```shell
czip
Enter the currency string (e.g., '1000USD to EUR'): 1000USD to EUR
Enter the date parameter (YYYYMMDD) or press Enter to skip: 
934.46EUR on 20240424
```
## API

You can start a local API with:

```shell
❯ uvicorn src.api.router:app --reload
INFO:     Will watch for changes in these directories: ['/Users/ricardoaugusto/dev/currency-zip']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [10881] using StatReload
INFO:     Started server process [10885]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Open on your browser http://127.0.0.1:8000. Optional host flag: `--host=192.168.1.123`.

Send a POST request like so:

```shell
curl --request POST \
  --url http://127.0.0.1:8000/convert \
  --header 'Content-Type: application/json' \
  --data '{
	"currency": "300EUR + 1500BRL to EUR",
	"when": "20240101"
}'
```

Check the full API Documentation here: http://127.0.0.1:8000/docs.

# Testing

```shell
pytest --cov=src/czip/tests --cov=src/api/tests --cov-report=html:src/tests/coverage
===== test session starts ======
platform darwin -- Python 3.12.0, pytest-8.1.1, pluggy-1.5.0
rootdir: /Users/ricardoaugusto/dev/currency-zip
plugins: cov-5.0.0, anyio-4.3.0
collected 24 items                                                                                                                          

src/api/tests/api_test.py .....                                                                                                       [ 20%]
src/czip/tests/czip_test.py ......                                                                                                    [ 45%]
src/czip/tests/unit_test.py .............                                                                                             [100%]

---------- coverage: platform darwin, python 3.12.0-final-0 ----------
Coverage HTML written to dir src/tests/coverage

===== 24 passed in 4.05s ======
```

# Contributing

Thank you for your interest in currency-zip! Before you start working and submit a PR, please review the instructions below.

- Lint your code with `black`
- Achieve 100% test coverage
- Make sure your tests pass
- Update the readme.md if needed

Thanks!