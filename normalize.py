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



def main():
    input_bytes = bytes(sys.stdin.buffer.read())
    input_unicode = input_bytes.decode('utf-8', 'replace')
    for row in csv.DictReader(input_unicode.split('\n')):
        print(row)
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
