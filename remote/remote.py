import requests

ret = requests.post('http://localhost/master/remote/master', json={
    'id': 'masterobj',
    'interval': 5
}).json()

print('created', ret)

requests.post('http://localhost/slave/remote/slave', json={
    'id': 'slaveobj',
    'key': ret['key'],
    'translations': {
        'buttons/buttonA': 'slaveButtons/buttonX'
    }
})
