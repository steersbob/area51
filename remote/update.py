import sys

import requests

args = [int(i) for i in sys.argv[1:]]

requests.put('http://localhost/master/objects/masterobj', json={
    'profiles': [1],
    'type': 'RemoteMaster',
    'data': {
        'buttons': {
            'buttonA': args[0],
            'buttonB': args[1],
            'buttonX': args[2],
            'buttonY': args[3],
        }
    }
})
