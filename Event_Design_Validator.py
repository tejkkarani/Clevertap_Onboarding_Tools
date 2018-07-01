import requests
import json
en = "test pressed"
ep = "Category"
epd = "String"
vn = ''
vp = ''
vpd = ''
t1 = '{"event_name":"'
t2 = en
t3 = '","from":'
t4 = str(20180101)
t5 = ',"to":'
t6 = str(20180604)
t7 = '}'
pay = t1 + t2 + t3 + t4 + t5 + t6 + t7
url = 'https://api.clevertap.com/1/events.json'
headers = {'X-CleverTap-Account-Id': '4W9-5K8-7R5Z', 'X-CleverTap-Passcode': 'ACS-JWW-IWKL', 'content-type': 'application/json'}
r = requests.post(url, data=pay, headers=headers)
j = json.loads(r.text)
if j['status'] != "success":
    vn='no'
else:
    vn='yes'
print(j)
x = j['cursor']
urlp = url + '?cursor=' + x
rr = requests.get(urlp, headers=headers)
jj = json.loads(rr.text)
print(jj)
k=0
kt=0
while k<len(jj['records']):
    try:
        po = jj['records'][k]['event_props'][ep]
        if (type(po) is unicode) and (not po.startswith('$D')):
            vpd = 'yes'
        else:
            vpd = 'no'
        kt = 1
    except:
        pass
    k = k+1
if kt == 1:
    vp = 'yes'
else:
    vp = 'no'
print(vn)
print(vp)
print(vpd)
