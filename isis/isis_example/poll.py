#!/usr/bin/env python3
"""
Code example for polling data from Spark services

Dependencies:
- requests
"""

from time import sleep

import requests
import urllib3
from requests.exceptions import ConnectionError, HTTPError

HOST = 'localhost'
SERVICE = 'spark-one'
URL = f'https://{HOST}/{SERVICE}/logged_objects'

urllib3.disable_warnings()

try:
    print('Polling services. To exit press Ctrl+C')
    while True:
        try:
            resp = requests.get(URL, verify=False)
            resp.raise_for_status()
            print(resp.json())
        except (HTTPError, ConnectionError) as ex:
            print(f'Error: {ex}')
        finally:
            sleep(10)
except KeyboardInterrupt:
    pass
