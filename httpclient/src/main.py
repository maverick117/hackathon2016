#!/usr/bin/python3
import requests
import json
import time

# POST data

with open('conf.json') as conf_file:
    conf = json.load(conf_file)

print(conf)
ip = conf['server_addr']
port = conf['server_port']
k = 0
#r = requests.post('http://192.168.199.191:8080/send',json=data)
while True:
    try:
        with open('stat.json') as data_file:
            data = json.load(data_file)
        print(data)
        r = requests.post('http://'+ip.strip()+':'+port.strip()+'/send',json=data)
        k = 0
        time.sleep(5)
    except requests.exceptions.ConnectionError:
        print("Connection Error.")
        print(k)
        if k < 60:
            k += k
        time.sleep(k)
    except KeyboardInterrupt:
        print('\nSIGINT received. Program terminated.')
        exit(0)
    
