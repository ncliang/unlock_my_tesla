#!/usr/bin/env python3

import argparse
import getpass
import time

import myTesla

parser = argparse.ArgumentParser(description='Unlock my tesla.')
parser.add_argument('--username', help='Tesla username', required=True)
parser.add_argument('--interval', help='Polling interval in seconds', default=300)

args = parser.parse_args()

password = getpass.getpass('Tesla password: ')

while True:
    conn = myTesla.connect(args.username, password)
    vehicle_state = conn.vehicle_state()

    if 'error' in vehicle_state:
        print(vehicle_state['error'])
    else:
        vehicle_state = vehicle_state['response']
        if vehicle_state['homelink_nearby'] and vehicle_state['locked']:
            conn.door_unlock()
            print('Found locked door. Unlock!')

    time.sleep(args.interval)
