#!/usr/bin/env python3
"""
Code example for subscribing to RabbitMQ messages from all Spark services

Dependencies:
- pika
"""

import json

import pika

HOST = 'localhost'
EXCHANGE = 'brewcast.history'


def callback(ch, method, properties, body):
    service_id = method.routing_key
    data = json.loads(body)
    print(f'Received {len(data)} blocks from {service_id}')


connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()
name = 'example_q'

channel.queue_declare(queue=name,
                      exclusive=True,
                      auto_delete=True)

channel.queue_bind(queue=name,
                   exchange=EXCHANGE,
                   routing_key='#')

channel.basic_consume(queue=name,
                      on_message_callback=callback,
                      auto_ack=True)

try:
    print('Waiting for messages. To exit press Ctrl+C')
    channel.start_consuming()
except KeyboardInterrupt:
    pass
