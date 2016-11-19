#!/usr/bin/python3
import requests
import json
import time
import os
import sys

# POST data
print('HTTP Client started')
try:
    with open(os.path.join(sys.path[0],'conf.json')) as conf_file:
        conf = json.load(conf_file)
except IOError:
    print('Could not open config file. Program terminated.')
    exit(0)
print('Current Configuration')
print(conf)
ip = conf['server_addr']
port = conf['server_port']
#r = requests.post('http://192.168.199.191:8080/send',json=data)
while True:
    try:
        with open(os.path.join(sys.path[0],'stat.json')) as data_file:
            data = json.load(data_file)
        print(data)
        print('POST in progress:')
        r_p = requests.post('http://'+ip.strip()+':'+port.strip()+'/send',json=data)
        print('GET in progress:')
        r_g = requests.get('http://'+ip.strip()+':'+port.strip()+'/rec')
        print(r_g.json())
        with open(os.path.join(sys.path[0],'data.json'),mode='w') as data_file:
            json.dump(r_g.json(),data_file)
        time.sleep(5)
    except requests.exceptions.ConnectionError:
        print("Connection Error.")
        time.sleep(30)
    except KeyboardInterrupt:
        print('\nSIGINT received. Program terminated.')
        exit(0)
    
