from time import sleep

import click
from paho.mqtt import client as mqtt


@click.command()
@click.pass_context
@click.option('--src-host', default='eventbus')
@click.option('--src-port', default=1883, type=int)
@click.option('--dest-host', default='172.17.0.1')
@click.option('--dest-port', default=9883, type=int)
def run(ctx, src_host, src_port, dest_host, dest_port):
    print(ctx.params)

    src_client = mqtt.Client()
    dest_client = mqtt.Client()

    src_client.user_data_set(f'src {src_host}:{src_port}')
    dest_client.user_data_set(f'dest {dest_host}:{dest_port}')

    def on_connect(client, userdata, flags, rc):
        print(f'on_connect {userdata} ({mqtt.error_string(rc)})')
        if client is src_client:
            src_client.subscribe('brewcast/history/#')

    def on_subscribe(client, userdata, mid, granted_qos):
        print(f'on_subscribe {userdata}')

    def on_message(client, userdata, message):
        if message.topic.endswith('/forwarded'):
            print('Ignoring forwarded message...')
            return
        dest_client.publish(message.topic + '/forwarded', message.payload)

    src_client.on_connect = on_connect
    src_client.on_message = on_message
    src_client.on_subscribe = on_subscribe

    dest_client.on_connect = on_connect
    dest_client.enable_bridge_mode()

    src_client.connect_async(src_host, src_port)
    dest_client.connect_async(dest_host, dest_port)

    src_client.loop_start()
    dest_client.loop_start()

    try:
        while True:
            sleep(3600)
    except KeyboardInterrupt:
        src_client.loop_stop()
        dest_client.loop_stop()


if __name__ == '__main__':
    run()
