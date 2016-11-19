#!/usr/bin/python3

import requests

# POST data
payload = {'abc':'123', 'def':'456'}
r = requests.post('http://192.168.199.191:8080/send',json=payload)

