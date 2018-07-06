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
    # this will return an ISO 8601 formatted timestamp with no timezone!
    # I'm not appending an offset because US/Eastern is not guaranteed to be a
    # constant number of hours offset from UTC
    return et.isoformat()

def convert_duration(duration):
    hours, minutes, seconds = duration.split(':')
    hours_secs = int(hours) * 60 * 60
    minutes_secs = int(minutes) * 60
    seconds_float = float(seconds)
    return hours_secs + minutes_secs + seconds_float

def handle_row(row):
    ts = normalize_timestamp(row['Timestamp'])
    address = row['Address']
    zip_code = row['ZIP'].rjust(5, '0')
    name = row['FullName'].upper()
    foo_duration = convert_duration(row['FooDuration'])
    bar_duration = convert_duration(row['BarDuration'])
    total_duration = foo_duration + bar_duration
    row['Timestamp'] = ts
    row['Address'] = address
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
    #print(input_bytes)
    #for i in input_bytes:
    #    print(type(i))
    #with open('tmp.csv', 'wb') as f:
    #    f.write(bytes(sys.stdin.buffer.read()))
    #with open('tmp.csv', 'rb') as fin:
    #    for i in fin:
    #        print(i.decode('utf-8', 'replace'))
    #foo = bytes(sys.stdin.buffer.read())
    #print(len(foo))
    #for i in foo:
    #    print(i)
    #bar = [x.decode('utf-8', 'replace') for x in foo]
    #print(bar)
    #input_bytes = [c.to_bytes(c.bit_length()+1, sys.byteorder) for c in sys.stdin.buffer.read()]
    #print(input_bytes)
    #input_bytes = bytearray()
    #sys.stdin.buffer.readinto(input_bytes)
    #print(input_bytes)
    #input_bytes = [c.to_bytes(1, sys.byteorder) for c in sys.stdin.buffer.read()]
    #unicode_csv = [b.decode('utf-8', 'replace') for b in input_bytes]
    #print(''.join(unicode_csv))
    #for line in sys.stdin.buffer.read():

        #print(line.to_bytes(1, sys.byteorder))
        #print(type(line))
        #print(line)
        #foo = sanitize(line.to_bytes(8, sys.byteorder))
        #print(foo)
        #print(line)
        #foo = line.decode('utf-8', 'replace')
        #foo = line.encode('utf-8', 'replace')
        ##print(foo.decode('utf-8'))

if __name__ == '__main__':
    main()
# first try reading the whole file to see if there's any invalid UTF-8
# if there is, replace the bogus characters with the unicode replacement character
# with open(file, 'rb') as f:
#   for i in f:
#     j = i.decode('utf-8', 'replace')
# once that's done, read the file using a csv.DictReader
# to pad zip codes:
# foo.rjust(5, '0')
