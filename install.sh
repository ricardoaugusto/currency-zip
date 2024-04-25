#!/bin/bash

if [ ! -f "./src/.env" ]; then
    echo "Error: .env file not found in /src directory. Aborting."
    exit 1
fi

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
czip_script="/usr/local/bin/czip"

cat > "$czip_script" <<EOF
#!/bin/bash

python_script="$script_dir/czip.py"

read -rp "Enter the currency string (e.g., '1000USD to EUR'): " currency_string
read -rp "Enter the date parameter (YYYYMMDD) or press Enter to skip: " date_param

if [ -n "\$date_param" ]; then
    python "\$python_script" "\$currency_string" --when="\$date_param"
else
    python "\$python_script" "\$currency_string"
fi
EOF

chmod +x "$czip_script"

echo "czip installed at $czip_script"
