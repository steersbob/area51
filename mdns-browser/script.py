from queue import Empty, Queue
from socket import inet_ntoa
from time import sleep

from zeroconf import ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf

BREWBLOX_DNS_TYPE = '_brewblox._tcp.local.'
DISCOVER_TIMEOUT_S = 5

def discover_wifi():
    queue: Queue[ServiceInfo] = Queue()
    conf = Zeroconf()

    def on_service_state_change(zeroconf: Zeroconf, service_type, name, state_change):
        if state_change == ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            queue.put(info)

    try:
        ServiceBrowser(conf, BREWBLOX_DNS_TYPE, handlers=[on_service_state_change])
        while True:
            info = queue.get(timeout=DISCOVER_TIMEOUT_S)
            if not info or not info.addresses or info.addresses == [b'\x00\x00\x00\x00']:
                continue  # discard simulators
            id = info.properties[b'ID'].decode()
            hw = info.properties[b'HW'].decode()
            host = inet_ntoa(info.addresses[0])
            yield {
                'connect': 'LAN',
                'id': id,
                'hw': hw,
                'host': host,
            }
    except Empty:
        pass
    finally:
        conf.close()


if __name__ == '__main__':
    while True:
        print('>>>>>>>>>')
        for dev in discover_wifi():
            print(' - '.join(dev.values()))
        print('<<<<<<<<<')
        sleep(10)
