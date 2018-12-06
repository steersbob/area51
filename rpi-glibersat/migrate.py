import json
import sys

import requests

HOST = 'http://localhost/datastore'


def main(filename):
    with open(filename) as f:
        content = json.load(f)

    for db_name, db_content in content.items():
        print(f'Creating database "{db_name}"')
        requests.put(f'{HOST}/{db_name}')

        for obj in db_content:
            obj['_id'] = obj['id']
            del obj['id']

        docs = {'docs': [obj for obj in db_content]}
        print(f'Filling database "{db_name}" with {len(db_content)} items')

        resp = requests.post(f'{HOST}/{db_name}/_bulk_docs', json=docs)
        print(resp.json())


if __name__ == '__main__':
    main(sys.argv[1])
