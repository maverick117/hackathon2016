#!/usr/bin/python3
import requests
import json
import time

# POST data
print('HTTP Client started')
with open('conf.json') as conf_file:
    conf = json.load(conf_file)
print('Current Configuration')
print(conf)
ip = conf['server_addr']
port = conf['server_port']
#r = requests.post('http://192.168.199.191:8080/send',json=data)
while True:
    try:
        with open('stat.json') as data_file:
            data = json.load(data_file)
        print(data)
        print('POST in progress:')
        r_p = requests.post('http://'+ip.strip()+':'+port.strip()+'/send',json=data)
        print('GET in progress:')
        r_g = requests.get('http://'+ip.strip()+':'+port.strip()+'/rec')
        print(r_g.json())
        with open('data.json',mode='w') as data_file:
            json.dump(r_g.json(),data_file)
        time.sleep(5)
    except requests.exceptions.ConnectionError:
        print("Connection Error.")
        time.sleep(30)
    except KeyboardInterrupt:
        print('\nSIGINT received. Program terminated.')
        exit(0)
    
