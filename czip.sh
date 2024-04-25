#!/bin/bash

python_script="czip.py"

read -rp "Enter the currency string (e.g., '1000USD to EUR'): " currency_string
read -rp "Enter the date parameter (YYYYMMDD) or press Enter to skip: " date_param

if [ -n "$date_param" ]; then
    python "$python_script" "$currency_string" --when="$date_param"
else
    python "$python_script" "$currency_string"
fi
