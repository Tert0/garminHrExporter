#!/usr/bin/env bash

rm -f export/stress-all.csv export/hrv-all.csv export/body-battery-all.csv

stress_header=$(cat export/*-stress.csv | head -n 1)
echo $stress_header > export/stress-all.csv
cat export/*-stress.csv | grep -v $stress_header >> export/stress-all.csv

hrv_header=$(cat export/*-hrv.csv | head -n 1)
echo $hrv_header > export/hrv-all.csv
cat export/*-hrv.csv | grep -v $hrv_header >> export/hrv-all.csv

body_battery_header=$(cat export/*-body-battery.csv | head -n 1)
echo $body_battery_header > export/body-battery-all.csv
cat export/*-body-battery.csv | grep -v $body_battery_header >> export/body-battery-all.csv

echo "generated: export/stress-all.csv export/hrv-all.csv export/body-battery-all.csv"
