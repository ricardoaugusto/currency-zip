# currency-zip

![version](https://img.shields.io/badge/version-v0.1.0-white) ![pytest](https://img.shields.io/badge/coverage-100%25-green)

# Purpose

To make banking/invoicing easier. Add currency conversion between multiple income sources and aggregate the total into a single currency.

# Install

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
$ which python
/Users/ricardoaugusto/dev/currency-zip/.venv/bin/python
```

Finally, install the `requirements.txt`:

```shell
pip install -r requirements.txt
```

# Usage

```shell
python czip.py "100EUR + 250USD + 1000BRL to GBP"
440.19GBP
```

<img width="377" alt="example-usage" src="https://github.com/ricardoaugusto/currency-zip/assets/7663281/b19b2955-3013-4b22-b0a0-076dbdaca2e0">

# Test

```shell
 pytest --cov=src tests --cov-report=html:tests/coverage
```

# Contribute