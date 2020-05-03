#!/usr/bin/env python3
"""
Code example for publishing data to the Brewblox eventbus

Dependencies:
- pika
"""

import json
from random import random
from time import sleep

import pika

HOST = 'localhost'
EXCHANGE = 'brewcast.history'

# This will be the top-level key in graphs / metrics
SERVICE = 'example'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

value = 20

try:
    while True:
        # Replace this with actual data
        # Nested data will be automatically flattened
        # See: https://brewblox.netlify.app/dev/reference/event_logging.html#history
        value += ((random() - 0.5) * 10)
        message = {'value[degC]': value}
        channel.basic_publish(exchange=EXCHANGE,
                              routing_key=SERVICE,
                              body=json.dumps(message))
        sleep(5)
        print(f'sent {message}')
except KeyboardInterrupt:
    connection.close()
