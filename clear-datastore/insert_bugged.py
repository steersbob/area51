import requests
import urllib3

urllib3.disable_warnings()

URL = 'https://localhost/datastore/brewblox-ui-store'

doc = {
    "_id": "layouts__4645f100-d9f3-8f8a-7bfc-1af4dc8d2286",
    "title": "Brewery Layout",
    "width": 20,
    "height": 15,
    "parts": [
        {
            "type": "Kettle",
            "id": "6b0f700c-bd68-56b0-0e16-4a46fa1d7328",
            "x": None,
            "y": None,
            "rotate": 0,
            "settings": {},
            "flipped": False
        }
    ]
}

resp = requests.post(URL, json=doc, verify=False)
print(resp.status_code, resp.content)
