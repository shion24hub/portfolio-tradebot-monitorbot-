import requests
from requests.auth import HTTPDigestAuth

data = {
    "name" : "shion",
    "etype" : "LIIMT",
}
url = "http://127.0.0.1:5000"
headers = {}
headers["Content-Type"]= 'application/json'

for passwd in ["1111", "2222"]:
    # r = requests.get('http://127.0.0.1:5000', auth=HTTPDigestAuth('shion', passwd))
    r = requests.post(
        url=url, 
        auth=HTTPDigestAuth('shion', passwd),
        headers=headers,
        json=data,
    )
    # print(r.status_code)
    # print(r.headers)
    # print(r.content)