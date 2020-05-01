# Getting started: Getting data from Brewblox

Required:
- Raspberry Pi or Linux-based desktop/laptop

## Install Brewblox

Follow the startup guide at https://brewblox.netlify.app/user/startup.html, but skip step 6 (Flashing the firmware).

Verify that the UI works by visiting *https://host_address* in your browser. The *spark-one* service will not be connected at this moment.

## Set up the Spark service simulator

In your Brewblox install directory (default: ~/brewblox), run the following command:

```
brewblox-ctl add-spark --name spark-one --force --simulation
```

The command will suggest to run `brewblox-ctl up`. Accept to do so, and then navigate back to the UI.
Wait a few seconds, and the *spark-one* service should now be available and connected.

## Add simulation sensors

Navigate to the *spark-one* service page in the UI, and create a *Temp Sensor (Mock)* block.

- Double click on the page background to bring up the block wizard.
- Scroll down and select *Temp Sensor (Mock)*.
- Choose a block name.
- Click the *Create* button.

Repeat as often as desired.

## Subscribe vs Poll

To get data from the system, you can choose to either listen to published RabbitMQ messages, or periodically fetch them from the service API.

We recommend subscribing to published messages, as it's more fault-tolerant, and will automatically adjust for new / different services.

## Subscribing to RabbitMQ messages

To access RabbitMQ from outside the Docker network, you'll have to expose a port for the eventbus service.

Edit the *docker-compose.yml* file, using either a text editor, or the `brewblox-ctl service editor` command.

Add the following configuration to the `services` object:

``` yaml
  eventbus:
    ports:
    - "5672:5672"
```

Example configuration:

``` yaml
services:
  spark-one:
    command: --name=spark-one --mdns-port=${BREWBLOX_PORT_MDNS} --discovery=all --simulation
    image: brewblox/brewblox-devcon-spark:${BREWBLOX_RELEASE}
    labels:
    - traefik.port=5000
    - 'traefik.frontend.rule=PathPrefix: /spark-one'
    privileged: true
    restart: unless-stopped
    volumes:
    - ./simulator__spark-one:/app/simulator
  eventbus:
    ports:
    - "5672:5672"
version: '3.7'
```

Example client code:

``` python
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

```

## Manually polling for data

This does not require any changes to the docker-compose.yml file.

Note that Brewblox uses a self-signed SSL certificate. To avoid errors, you'll have to either use it in your client, or disable SSL verification.

Example code:

``` python
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
```
