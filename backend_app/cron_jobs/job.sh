#!/usr/bin/env bash

name_var=big_mac
date_var=$(echo -n `date +"%Y-%m-%d"`)
price_var=$(python3 scripts/big_mac_parser.py)
echo $price_var

curl -X 'POST' \
  'http://127.0.0.1:8000/add_entries' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "'"$name_var"'",
    "date": "'"$date_var"'",
    "price": "'$price_var'"
  }'

name_var=cheeseburger
date_var=$(echo -n `date +"%Y-%m-%d"`)
price_var=$(python3 scripts/cheeseburger_parser.py)
echo $price_var

curl -X 'POST' \
  'http://127.0.0.1:8000/add_entries' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "'"$name_var"'",
    "date": "'"$date_var"'",
    "price": "'$price_var'"
  }'

name_var=diesel
date_var=$(echo -n `date +"%Y-%m-%d"`)
price_var=$(python3 scripts/diesel_parser.py)
echo $price_var

curl -X 'POST' \
  'http://127.0.0.1:8000/add_entries' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "'"$name_var"'",
    "date": "'"$date_var"'",
    "price": "'$price_var'"
  }'

# curl http://127.0.0.1:8000/