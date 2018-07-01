import requests
import json
en = "test pressed"
pay = '{"event_name":"test pressed","from":20180101,"to":20180604}'
url = 'https://api.clevertap.com/1/events.json'
headers = {'X-CleverTap-Account-Id': '4W9-5K8-7R5Z', 'X-CleverTap-Passcode': 'ACS-JWW-IWKL', 'content-type': 'application/json'}
r = requests.post(url, data=pay, headers=headers)
j = json.loads(r.text)
print(j)
