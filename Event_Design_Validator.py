import requests
import json
import chilkat
import sys
import unicodecsv as csv
en = []
ep = []
epd = []


def csv_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        en.append(line['Event Name'])
        ep.append(line['Event Property'])
        epd.append(line['Event Property Data Type'])


csv_path = "Events.csv"
with open(csv_path) as f_obj:
    csv_reader(f_obj)
vpd = [None]*len(en)
vn = []
vp = []
i = 0
while i < len(en):
    if en[i] == '' and ep[i] == '' and epd[i] == '':
        vn.append('')
        vp.append('')
        vpd[i] = ''
        i = i+1
        continue
    t1 = '{"event_name":"'
    if en[i] != '':
        t2 = en[i]
    t3 = '","from":'
    t4 = str(20180101)
    t5 = ',"to":'
    t6 = str(20180615)
    t7 = '}'
    pay = t1 + t2 + t3 + t4 + t5 + t6 + t7
    url = 'https://api.clevertap.com/1/events.json'
    headers = {'X-CleverTap-Account-Id': '4W9-5K8-7R5Z', 'X-CleverTap-Passcode': 'ACS-JWW-IWKL', 'content-type': 'application/json'}
    r = requests.post(url, data=pay, headers=headers)
    j = json.loads(r.text)
    if j['status'] != "success":
        if en[i] != '':
            vn.append('no')
            vp.append('no')
            vpd[i] = 'no'
        else:
            vn.append('')
            vp.append('no')
            vpd[i] = 'no'
        i = i+1
        continue
    else:
        if en[i] != '':
            vn.append('yes')
        else:
            vn.append('')
    print(j)
    x = j['cursor']
    urlp = url + '?cursor=' + x
    rr = requests.get(urlp, headers=headers)
    jj = json.loads(rr.text)
    print(jj)
    k = 0
    kt = 0
    if ep[i] != '':
        try:
            while k < len(jj['records']):
                try:
                    po = jj['records'][k]['event_props'][ep[i]]
                    if (type(po) is unicode) and (not po.startswith('$D')):
                        vpd[i] = 'yes'
                    else:
                        vpd[i] = 'no'
                    kt = 1
                except:
                    pass
                k = k+1
        except:
            pass
    try:
        nextc = jj['next_cursor']
    except:
        nextc = ''
    while nextc != '':
        urlp = url + '?cursor=' + nextc
        rr = requests.get(urlp, headers=headers)
        jj = json.loads(rr.text)
        k = 0
        if ep[i] != '':
            try:
                while k < len(jj['records']):
                    try:
                        po = jj['records'][k]['event_props'][ep[i]]
                        if (type(po) is unicode) and (not po.startswith('$D')):
                            vpd[i] = 'yes'
                        else:
                            vpd[i] = 'no'
                        kt = 1
                    except:
                        pass
                    k = k + 1
            except:
                pass
        try:
            nextc = jj['next_cursor']
        except:
            nextc = ''
    if ep[i] != '':
        if kt == 1:
            vp.append('yes')
        else:
            vp.append('no')
            vpd[i] = 'no'
    i = i+1
print(vn)
print(vp)
print(vpd)
csv = chilkat.CkCsv()
csv.put_HasColumnNames(True)
success = csv.LoadFile(csv_path)
if success != True:
    print(csv.lastErrorText())
    sys.exit()
i = 0
while i < len(en):
    success = csv.SetCell(i, 8, vn[i])
    success = csv.SetCell(i, 9, vp[i])
    success = csv.SetCell(i, 10, vpd[i])
    i = i+1
csvDoc = csv.saveToString()
success = csv.SaveFile(csv_path)
if success != True:
    print(csv.lastErrorText())
