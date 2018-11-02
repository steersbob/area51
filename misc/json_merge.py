#! /bin/env python3

import json
import sys


def main(file_a_name, file_b_name, file_out_name):
    with open(file_a_name) as f:
        file_a_content = json.load(f)

    with open(file_b_name) as f:
        file_b_content = json.load(f)

    b_ordered = {v['DeviceUI']: v for v in file_b_content}
    output = []

    for val in file_a_content:
        dev = b_ordered.get(val['DevEUI'])
        if dev:
            val['SensorID'] = dev['SensorID']
            val['DataType'] = dev['DataType']
            output.append(val)

    print(f'A size: {len(file_a_content)}')
    print(f'B size: {len(file_b_content)}')
    print(f'Output size: {len(output)}')

    with open(file_out_name, 'w') as f:
        json.dump(output, f)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(*sys.argv[1:])
    else:
        print('Required arguments: file A, file B, output file')
