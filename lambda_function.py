import os
import time

import common
import myTesla


def lambda_handler(event, _):
    username = os.environ['TESLA_EMAIL']
    password = os.environ['TESLA_PASS']

    conn = myTesla.connect(username, password)
    vehicles = common.make_request(conn.vehicles)

    for v in vehicles:
        common.make_request(conn.select_vehicle, {'vin': v['vin']})

        if v['state'] != 'online':
            print('%s asleep, waking...' % v['display_name'])
            common.make_request(conn.wake_up)
            time.sleep(5)  # HACK - wait for it to wake up...

    if event['clickType'] == 'SINGLE':
        common.make_request(conn.door_unlock)
    elif event['clickType'] == 'DOUBLE':
        common.make_request(conn.trunk_open, {'which_trunk': 'front'})
