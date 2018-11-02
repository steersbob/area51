"""
Fires a bunch of create requests at a spark service to measure throughput
"""

import asyncio

from aiohttp import ClientSession

URL = 'http://localhost:5000/spark'


async def create(session, id):
    return await session.post(URL + '/objects', json={
        'id': id,
        'profiles': [1],
        'type': 'OneWireTempSensor',
        'data': {
            'settings': {
                'address': 'FF',
                'offset[delta_degC]': 20
            },
            'state': {
                'value[delta_degF]': 100,
                'connected': True
            }
        }
    })


async def run():
    async with ClientSession(raise_for_status=True) as session:
        num_items = 100
        coros = [create(session, f'object{id}') for id in range(num_items)]
        responses = await asyncio.gather(*coros)
        print(len(responses))

        await session.post(URL + '/profiles', json=[1])

        coros = [session.get(URL + '/objects') for _ in range(num_items)]
        await asyncio.gather(*coros)
        retv = await session.get(URL + '/objects')
        print(len(await retv.json()))


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()


if __name__ == '__main__':
    main()
