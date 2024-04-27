#!/usr/bin/env python3

import garth
import yaml
import json
import os
import argparse
import datetime

from dateutil import parser as date_parser
from garth.exc import GarthException
from getpass import getpass

HEART_RATE_PATH = "/wellness-service/wellness/dailyHeartRate"

# the config structure
config = {
    'exportDir': '',
    'tokenDir': '',
}

# load the config file and store it in the config structure
def loadConfig():
    global config

    with open('config.yaml') as file:
        config = yaml.safe_load(file)

# get the real path of the export directory and create it if it doesn't exist
def ensureExportDir():
    global config
    
    exportDir = os.path.realpath(config['exportDir'])
    if not os.path.exists(exportDir):
        os.makedirs(exportDir)
    return exportDir

# get the real path of the token directory and create it if it doesn't exist
def ensureTokenDir():
    global config
    
    tokenDir = os.path.realpath(config['tokenDir'])
    if not os.path.exists(tokenDir):
        os.makedirs(tokenDir)
    return tokenDir

def connect_api(client: garth.Client, path, **kwargs):
    return client.connectapi(path, **kwargs)

def get_hr_zone(config: dict, hr: int):
    hr_zones = config['zones']
    for zone in hr_zones:
        if hr >= zone['min'] and hr <= zone['max']:
            return zone['name']
    return 'unknown'

loadConfig()

export_dir = ensureExportDir()
token_dir = ensureTokenDir()

print('Export directory:', export_dir)
print('Token directory:', token_dir)


try:
    garth.resume(token_dir)
    garth.client.username
except:
    email = input('Enter your Garmin Connect email: ')
    password = getpass('Enter your Garmin Connect password: ')
    garth.client.login(email, password)

garth.save(token_dir)
display_name = garth.client.profile["displayName"]

print('Garmin Login successful!')

# parse the date from the command line
# if the date is not provided, the current date is used


parser = argparse.ArgumentParser(description='Export Garmin heart rate data')
parser.add_argument('date', type=lambda s: date_parser.parse(s), help='The date for which the heart rate is exported', default=datetime.datetime.today().isoformat(), nargs='?')

args = parser.parse_args()
date = args.date

print('Exporting heart rate data for', date.date())

# get the heart rate data for the given date
url = f'{HEART_RATE_PATH}/{display_name}'
params = {
    'date': date.date().isoformat()
}

heart_rate_data = connect_api(garth.client, url, params=params)

# save the heart rate data to a file in the export directory
# if the file already exists, it will be overwritten
# the name of the file is the date in the format YYYY-MM-DD.json
filename = os.path.join(export_dir, date.date().isoformat() + '.json')
with open(filename, 'w') as file:
    file.write(json.dumps(heart_rate_data, indent=4))

print('Raw Heart rate data exported to', filename)

# convert the heart rate data to a CSV file
# the CSV file has the following columns:
# - timestamp: the timestamp of the heart rate data
# - heart_rate: the heart rate value
# the CSV file is saved in the export directory with the name YYYY-MM-DD.csv
filename = os.path.join(export_dir, date.date().isoformat() + '.csv')
with open(filename, 'w') as file:
        file.write('timestamp,date,heart_rate,zone\n')
        for entry in heart_rate_data['heartRateValues']:
            timestamp = entry[0]
            value = entry[1]
            if value is None:
                continue
            # convert the timestamp to a human-readable format
            date_formatted = datetime.datetime.fromtimestamp(timestamp / 1000).isoformat()
            zone = get_hr_zone(config, value)
           
            file.write(f"{timestamp},{date_formatted},{value},{zone}\n")

print('CSV Heart rate data exported to', filename)

# calculate the percentage of time spent in each heart rate zone
# the heart rate zones are defined in the config file
# the result is saved to a file in the export directory with the name YYYY-MM-DD-zones.json
zones = {}
for entry in heart_rate_data['heartRateValues']:
    value = entry[1]
    if value is None:
        continue
    zone = get_hr_zone(config, value)
    if zone not in zones:
        zones[zone] = 0
    zones[zone] += 1

total = sum(zones.values())
for zone, count in zones.items():
    zones[zone] = count / total

filename = os.path.join(export_dir, date.date().isoformat() + '-zones.json')
with open(filename, 'w') as file:
    file.write(json.dumps(zones, indent=4))

print('Heart rate zones exported to', filename)

# print the result
print('Heart rate zones:')
for zone, percentage in zones.items():
    print(f'{zone}: {percentage:.2%}')


# get the HRV data for the given date
url = f'/hrv-service/hrv/{date.date().isoformat()}'
hrv_data = connect_api(garth.client, url)

# save the HRV data to a file in the export directory
# if the file already exists, it will be overwritten
# the name of the file is the date in the format YYYY-MM-DD-hrv.json
filename = os.path.join(export_dir, date.date().isoformat() + '-hrv.json')
with open(filename, 'w') as file:
    file.write(json.dumps(hrv_data, indent=4))

print('HRV data exported to', filename)

# get the stress data for the given date
url = f'/wellness-service/wellness/dailyStress/{date.date().isoformat()}'
stress_data = connect_api(garth.client, url, params=params)

# save the stress data to a file in the export directory
# if the file already exists, it will be overwritten
# the name of the file is the date in the format YYYY-MM-DD-stress.json
filename = os.path.join(export_dir, date.date().isoformat() + '-stress.json')
with open(filename, 'w') as file:
    file.write(json.dumps(stress_data, indent=4))

print('Stress data exported to', filename)

# get the sleep data for the given date
url = f'/wellness-service/wellness/dailySleepData/{display_name}'
params = {
    'date': date.date().isoformat(),
    "nonSleepBufferMinutes": 60
}
sleep_data = connect_api(garth.client, url, params=params)

# save the sleep data to a file in the export directory
# if the file already exists, it will be overwritten
# the name of the file is the date in the format YYYY-MM-DD-sleep.json
filename = os.path.join(export_dir, date.date().isoformat() + '-sleep.json')
with open(filename, 'w') as file:
    file.write(json.dumps(sleep_data, indent=4))

print('Sleep data exported to', filename)
