"""
Code example for publishing data to the Brewblox eventbus

Dependencies:
- paho-mqtt
"""

import json
import re
import subprocess
from random import random
from time import sleep

from paho.mqtt import client as mqtt

# 172.17.0.1 is the default IP address for the host running the Docker container
# Change this value if Brewblox is installed on a different computer
HOST = '172.17.0.1'

# 80 is the default port for HTTP, but this can be changed in brewblox env settings.
PORT = 80

# This is a constant value. You never need to change it.
HISTORY_TOPIC = 'brewcast/history'

# The history service is subscribed to all topics starting with 'brewcast/history'
# We can make our topic more specific to help debugging
TOPIC = HISTORY_TOPIC + '/pi-temperature'

# Create a websocket MQTT client
client = mqtt.Client(transport='websockets')
client.ws_set_options(path='/eventbus')

def check_cpu_temperature():
    raw_output = subprocess.check_output(
        ["/opt/vc/bin/vcgencmd", "measure_temp"]
    ).decode()
    output_matching = re.search("temp=([\d\.]+)'C", raw_output)
    return float(output_matching.group(1))

try:
    client.connect_async(host=HOST, port=PORT)
    client.loop_start()

    while True:
        message = {
            'key': 'pi-temperature',
            'data': {'temperature[degC]': check_cpu_temperature()}
        }

        client.publish(TOPIC, json.dumps(message))
        sleep(10)

finally:
    client.loop_stop()
