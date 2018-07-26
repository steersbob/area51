import requests

requests.post('http://localhost/master/objects', json={
    'id': 'masterobj',
    'profiles': [1],
    'type': 'RemoteMaster',
    'data': {
        'buttons': {
            'buttonA': 1
        }
    }
})

requests.post('http://localhost/slave/objects', json={
    'id': 'slaveobj',
    'profiles': [1],
    'type': 'RemoteSlave',
    'data': {
        'slaveButtons': {
            'buttonA': 5
        }
    }
})

requests.post('http://localhost/master/profiles', json=[1])
requests.post('http://localhost/slave/profiles', json=[1])
