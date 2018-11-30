import os
import time

import myTesla


class UnlockException(Exception):
    pass


def make_request(callable, callable_args=None, max_attempts=1, retry_interval_sec=5):
    if not callable_args:
        callable_args = {}

    for attempt in range(max_attempts):
        resp = callable(**callable_args)
        if not resp:
            return None

        if 'error' in resp:
            if attempt == max_attempts - 1:
                raise UnlockException(resp['error'])
            else:
                time.sleep(retry_interval_sec * (attempt + 1))
                continue

        return resp['response']


def lambda_handler(event, _):
    username = os.environ['TESLA_EMAIL']
    password = os.environ['TESLA_PASS']

    conn = myTesla.connect(username, password)
    vehicles = make_request(conn.vehicles)

    for v in vehicles:
        make_request(conn.select_vehicle, {'vin': v['vin']})

        if v['state'] != 'online':
            print('%s asleep, waking...' % v['display_name'])
            make_request(conn.wake_up)

        if event['clickType'] == 'SINGLE':
            make_request(conn.door_unlock, max_attempts=3)
        elif event['clickType'] == 'DOUBLE':
            make_request(conn.trunk_open, {'which_trunk': 'front'}, max_attempts=3)
