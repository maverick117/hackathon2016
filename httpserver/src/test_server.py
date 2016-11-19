#!/usr/bin/python3

import requests

# POST data
payload = {'abc':'123', 'def':'456'}
r_p = requests.post('http://192.168.199.191:8080/send',json=payload)

r_g = requests.get('http://localhost:8080/rec')
print(r_g)
