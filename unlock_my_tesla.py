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


class UnlockException(Exception):
    pass


def make_request(callable, callable_args=None):
    if not callable_args:
        callable_args = {}

    resp = callable(**callable_args)
    if not resp:
        return None

    if 'error' in resp:
        raise UnlockException(resp['error'])
    return resp['response']


print('Checking for locked and at home cars at %s second intervals...' % args.interval)

while True:
    conn = myTesla.connect(args.username, password)
    vehicles = make_request(conn.vehicles)

    for v in vehicles:
        if v['state'] != 'online':
            print('%s offline, skipped' % v['display_name'])
            continue

        make_request(conn.select_vehicle, {'vin': v['vin']})
        vehicle_state = make_request(conn.vehicle_state)
        if vehicle_state['homelink_nearby'] and vehicle_state['locked']:
            make_request(conn.door_unlock)
            print('%s door locked and at home. Unlock!' % v['display_name'])

    time.sleep(args.interval)
