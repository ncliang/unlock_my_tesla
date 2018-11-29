#!/usr/bin/env python3

import argparse
import getpass
import time

import common
import myTesla

parser = argparse.ArgumentParser(description='Unlock my tesla.')
parser.add_argument('--username', help='Tesla username', required=True)
parser.add_argument('--interval', help='Polling interval in seconds', default=300)

args = parser.parse_args()

password = getpass.getpass('Tesla password: ')

print('Checking for locked and at home cars at %s second intervals...' % args.interval)

while True:
    conn = myTesla.connect(args.username, password)
    vehicles = common.make_request(conn.vehicles)

    for v in vehicles:
        if v['state'] != 'online':
            print('%s offline, skipped' % v['display_name'])
            continue

        common.make_request(conn.select_vehicle, {'vin': v['vin']})
        vehicle_state = common.make_request(conn.vehicle_state)
        if vehicle_state['homelink_nearby'] and vehicle_state['locked']:
            common.make_request(conn.door_unlock)
            print('%s door locked and at home. Unlock!' % v['display_name'])

    time.sleep(args.interval)
