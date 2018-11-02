import requests

URL = 'http://localhost:9000'

v = requests.post(URL + '/spark/objects', json={
    'id': 'testobj',
    'profiles': [1],
    'type': 'OneWireTempSensor',
    'data': {
        'settings': {
            'address': 'FF'
        }
    }
})
print(v, v.text)

v = requests.post(URL + '/spark/profiles', json=[1])
print(v, v.text)

v = requests.post(URL + '/history/_debug/query', json={
    'query': 'CREATE RETENTION POLICY testretention ON brewblox DURATION 10w REPLICATION 1'
})
print(v, v.text)

# v = requests.post(URL + '/history/_debug/query', json={
#     'query': 'SELECT * FROM brewblox.spark.testretention'
# })
# print(v, v.text)
