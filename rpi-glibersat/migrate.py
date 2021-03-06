import json
import sys

import requests

HOST = 'http://localhost/datastore'


def main(filename):
    with open(filename) as f:
        content = json.load(f)

    for db_name, db_content in content.items():
        print('Creating database "{}"'.format(db_name))
        requests.put([HOST, db_name].join('/'))

        for obj in db_content:
            obj['_id'] = obj['id']
            del obj['id']

        docs = {'docs': [obj for obj in db_content]}
        print('Filling database "{}" with {} items'.format(db_name, len(db_content)))

        resp = requests.post('{}/{}/_bulk_docs'.format(HOST, db_name), json=docs)
        print(resp.json())


if __name__ == '__main__':
    main(sys.argv[1])
