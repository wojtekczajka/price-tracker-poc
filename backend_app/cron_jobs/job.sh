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

# RTX-4060-TI
item_id=4
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/rtx_4060_ti_parser.py)
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

# IPHONE-14-BLUE-128
item_id=5
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/iphone_14_blue_128_parser.py)
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

# MAKA-BASIA-POZ-T500-1KG
item_id=6
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/maka_basia_poz_t500_1kg_parser.py)
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

# 3-BIT-46G
item_id=7
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/3_bit_46g_parser.py)
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

# AHMADTEA-EARLGREY-CZARNY-100G
item_id=8
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/ahmadtea_earlgrey_cz_100g_parser.py)
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

# AIRWAVES-XXL-36
item_id=9
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/airwaves_xxl_36_parser.py)
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

# ALPENGOLD_NUSSBEISER_CZEKOLADA_100G
item_id=10
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/alpengold_nussbeiser_czekolada_100g_parser.py)
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

# AMINO-ROSOL-59G
item_id=11
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/amino_rosol_59g_parser.py)
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

# BAKOMA-JOGURT-GRECKI-440G
item_id=12
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/bakoma_jogurt_grecki_440g_parser.py)
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

# CHEETOS-KETCHUP-85G
item_id=13
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/cheetos_ketchup_85g_parser.py)
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

# COCACOLA-1-5-L
item_id=14
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/coca_cola_1_5_l_parser.py)
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

# PALUSZKI-BESKIDZKIE-SOL-70G
item_id=15
date_var=$(date +"%Y-%m-%d")
price_var=$(python3 scripts/paluszki_beskidzkie_sol_70g_parser.py)
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
