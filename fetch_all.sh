#!/usr/bin/env bash

: ${1?"Usage: $0 YYYY-MM-DD"}

start=$1

start=$(date -d $start +%Y%m%d)
end=$(date +%Y%m%d)

while [[ $start -le $end ]]
do
        echo $(date -d $start +%Y-%m-%d)
        python garminHrExporter.py $(date -d $start +%Y-%m-%d)
        start=$(date -d"$start + 1 day" +"%Y%m%d")
done
