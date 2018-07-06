#!/usr/bin/env python3

import csv
import datetime
import sys
import time

import pytz

def normalize_timestamp(time_string):
    dt = datetime.datetime.strptime(time_string, '%m/%d/%y %I:%M:%S %p')
    pacific = pytz.timezone('US/Pacific')
    eastern = pytz.timezone('US/Eastern')
    # localize the datetime object to 'US/Pacific'
    pt = pacific.localize(dt)
    # convert to 'US/Eastern'
    et = pt.astimezone(eastern)
    return et.isoformat()

def convert_duration(duration):
    hours, minutes, seconds = duration.split(':')
    hours_secs = int(hours) * 60 * 60
    minutes_secs = int(minutes) * 60
    seconds_float = float(seconds)
    return hours_secs + minutes_secs + seconds_float

def handle_row(row):
    ts = normalize_timestamp(row['Timestamp'])
    zip_code = row['ZIP'].rjust(5, '0')
    name = row['FullName'].upper()
    foo_duration = convert_duration(row['FooDuration'])
    bar_duration = convert_duration(row['BarDuration'])
    total_duration = foo_duration + bar_duration
    row['Timestamp'] = ts
    row['ZIP'] = zip_code
    row['FullName'] = name
    row['FooDuration'] = foo_duration
    row['BarDuration'] = bar_duration
    row['TotalDuration'] = total_duration
    return row


def main():
    input_bytes = bytes(sys.stdin.buffer.read())
    input_unicode = input_bytes.decode('utf-8', 'replace')
    normalized_rows = []
    reader = csv.DictReader(input_unicode.split('\n'))
    for row in reader:
        try:
            new_row = handle_row(row)
            normalized_rows.append(new_row)
        except:
            sys.stderr.write('Error parsing row!\n')
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
    writer.writeheader()
    for normalized_row in normalized_rows:
        writer.writerow(normalized_row)

if __name__ == '__main__':
    main()
