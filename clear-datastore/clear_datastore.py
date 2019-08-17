import requests
import urllib3

urllib3.disable_warnings()

URL = 'https://localhost/datastore/brewblox-ui-store'

all_docs = requests.get('{}/_all_docs'.format(URL),
                        params={'include_docs': 'true'},
                        verify=False
                        ).json()

layout_docs = [
    d for d in all_docs['rows']
    if d['id'].startswith('layouts')
]
faulty = []  # (id, rev)

for document in layout_docs:
    doc = document['doc']
    if next((part for part in doc['parts'] if part['x'] is None), None):
        faulty.append((doc['_id'], doc['_rev']))

print('Removing {} document{}'.format(
    len(faulty), 's' if len(faulty) != 1 else ''))

for (id, rev) in faulty:
    requests.delete('{}/{}'.format(URL, id),
                    params={'rev': rev},
                    verify=False)
