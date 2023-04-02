#!/usr/bin/env bash

# CHEESBURGER
item_id=1
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/cheeseburger_parser.py)
echo $price_var

curl -X 'POST' \
  'http://127.0.0.1:8000/add_entries/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "item_id": '$item_id',
    "date": "'"$date_var"'",
    "price": "'$price_var'"
  }'

# DIESEL
item_id=2
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/diesel_parser.py)
echo $price_var

curl -X 'POST' \
  'http://127.0.0.1:8000/add_entries/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "item_id": '$item_id',
    "date": "'"$date_var"'",
    "price": "'$price_var'"
  }'

# BIG-MAC
item_id=3
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/big_mac_parser.py)
echo $price_var

curl -X 'POST' \
  'http://127.0.0.1:8000/add_entries/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "item_id": '$item_id',
    "date": "'"$date_var"'",
    "price": "'$price_var'"
  }'

# curl http://127.0.0.1:8000/
