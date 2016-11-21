#!/usr/bin/env python3
from __future__ import print_function
import urllib
import urllib.parse
import urllib.request
import http.client
import string, random
import json
import getpass
import time

#======================================================
username = 'lixy'
password = 'lixy'
#======================================================
lang = 'EN'
#======================================================

httpClient = None
try:
	print('')
	print(u'account got.')
	print(u'========================================')

	while True:
		#======================================================
		#Define
		url="https://controller.shanghaitech.edu.cn:8445/PortalServer/Webauth/webAuthAction!login.action"
		params = urllib.parse.urlencode({'userName': username, 'password':password,'hasValidateCode':False,'authLan':'zh_CN'})
		cookie_code = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 32)).replace(' ','')
		headers = {'Content-type': 'application/x-www-form-urlencoded'
						, 'Accept': '*/*','Cookie':'JSESSIONID=' + cookie_code}
		httpClient = http.client.HTTPSConnection('controller.shanghaitech.edu.cn', 8445, timeout=30)
		#======================================================

		print(u'Logining......',end="")
		httpClient.request('POST', '/PortalServer/Webauth/webAuthAction!login.action', params, headers)
		response = httpClient.getresponse()
		if response.status != 200:
			print(u'Connection Failed! Is the network available?')
			connect()
			exit()
		else:
			response_data = response.read().decode('utf-8')
			response_data_json = json.loads(response_data)
			if response_data_json['success'] != True:
				print(u'Login Failed! Is your account available?')
				print(response_data)
				exit()
			else:
				print(u'Success!')
				print(u'Username:' + response_data_json['data']['account'])
				print(u'ClientIP:' + response_data_json['data']['ip'])

		print(u'========================================')
		#======================================================
		#Define
		params2 = urllib.parse.urlencode({'userName': username, 'clientIp':response_data_json['data']['ip']})
		#======================================================

		timer = 0
		while True:
			if timer==10:
				break
			timer=timer+1
			print(u'Heartbeat......',end='')
			httpClient.request('POST', '/PortalServer/Webauth/webAuthAction!hearbeat.action', params2, headers)
			response = httpClient.getresponse()
			if response.status != 200:
				print(u'Connection Failed! Is the network available?')
				break
			else:
				response_data = response.read().decode('utf-8')
				response_data_json = json.loads(response_data)
				if response_data_json['success'] != True:
				    print(u'Failed! Is your account available?')
				    print(response_data)
				    break
				else:
					print(u'Success!')
			time.sleep(120)
		print(u'========================================')

except Exception as e:
	print(u'Unknown Error! Is the network available?')
	print(e)
finally:
	if httpClient:
		httpClient.close()
