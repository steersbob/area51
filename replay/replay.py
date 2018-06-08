import argparse
import asyncio
from collections import namedtuple

import aiofiles
from aiohttp import ClientSession

DENSITY = 0.9982
GRAVITY = 9.81
CALIBRATION_VOLTAGE = [-4.688512282592881, -4.807393316657185]
VOLTAGE_SENSITIVITY = [-468851.2865805399, -459340.85991038586]
NAMES = ['lower_sensor', 'upper_sensor']
BITS_PER_MBAR = 52429

INPUT = 'input.csv'

KEYS = [
    'sensor_id',
    'value_1s',
    'value_30s',
    'voltage_1s',
    'voltage_30s',
    'unfiltered',
]

Measurement = namedtuple('Measurement', KEYS)


def calculate_values(raw,
                     voltage,
                     calibration_voltage,
                     voltage_sensitivity,
                     bits_per_mbar
                     ) -> dict:

    compensated = raw - (voltage - calibration_voltage) * voltage_sensitivity
    pressure = compensated / bits_per_mbar
    height = pressure / (DENSITY * GRAVITY)

    return dict(
        raw=raw,
        voltage=voltage,
        compensated=compensated,
        pressure=pressure,
        height=height
    )


def from_measurement(measurement: Measurement) -> dict:
    idx = measurement.sensor_id

    name = NAMES[idx]
    calibration_voltage = CALIBRATION_VOLTAGE[idx]
    voltage_sensitivity = VOLTAGE_SENSITIVITY[idx]

    return {
        name: {
            'output': {
                'updated_1s': calculate_values(
                    measurement.value_1s,
                    measurement.voltage_1s,
                    calibration_voltage,
                    voltage_sensitivity,
                    BITS_PER_MBAR
                ),
                'updated_30s': calculate_values(
                    measurement.value_30s,
                    measurement.voltage_30s,
                    calibration_voltage,
                    voltage_sensitivity,
                    BITS_PER_MBAR
                )}
        }

    }


async def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--address', default='http://localhost/history', help='[%(default)s]')
    argparser.add_argument('--measurement', default='pressure', help='[%(default)s]')
    args = argparser.parse_args()

    current = dict()

    print('Reading from ' + INPUT)

    async with aiofiles.open(INPUT) as f, ClientSession() as client:
        while True:
            line = await f.readline()
            meas = Measurement(*[int(v) for v in line.split(',')[1:]])

            current.update(from_measurement(meas))
            await client.post(args.address + '/_debug/publish', json={
                'exchange': 'brewcast',
                'routing': args.measurement,
                'message': current
            })

            await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
