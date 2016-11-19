#!/usr/bin/python
from upm import pyupm_i2clcd as lcd
from upm import pyupm_rfr359f as upmRfr359f
from upm import pyupm_rpr220 as upmRpr220
import time
import serial
import json
import os,sys

def ChangeDisplay1(_color,_text):
    myLcd.setCursor(0,0)
    if _color=='same':
        myLcd.write(_text+space)
    elif _color=='green':
        myLcd.setColor(0,255,0)
        myLcd.write(_text+space)
    elif _color=='yellow':
        myLcd.setColor(255,185,15)
        myLcd.write(_text+space)
    elif _color=='red':
        myLcd.clear()
        myLcd.setColor(255, 0, 0)
        myLcd.write(_text+space)
    else :
        myLcd.clear()
        myLcd.setColor(255, 0, 0)
        myLcd.write('unknown error'+space)

def ChangeDisplay2(_text):
    myLcd.setCursor(1,0)
    myLcd.write(_text+space)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.setCursor(0,0)
myDistInterrupter1 = upmRfr359f.RFR359F(2)
myDistInterrupter2 = upmRfr359f.RFR359F(3)
myReflectiveSensor1 = upmRpr220.RPR220(4)
myReflectiveSensor2 = upmRpr220.RPR220(5)
#data="{'rate': 0, 'state_code': 0, 'id': '0x01', 'volume': 0, 'package_type': 0, 'emergency_type': 0, 'longtitude':+121.5952285, 'latitude':+31.1767925, 'elevation':2}"
space=' '*16

#ser.write("testing")
try:
    while 1:
        response = ser.readline()
        if ';' not in response:
            continue
        res=response.split(';')
        print res
        if (myDistInterrupter1.objectDetected() and myDistInterrupter2.objectDetected()):
            ChangeDisplay1('red','Full')
            print "Full"
        else:
            if res[0]=='True':
                print 't'
                ChangeDisplay1('yellow','trash out')
            else:
                print 'f'
                ChangeDisplay1('green','OK')
            ChangeDisplay2('Flowrate='+str(int(res[1])))
        try:
            with open(os.path.join(sys.path[0],'stat.json')) as data_file:
                data = json.load(data_file)
                print data
                #changevalue here

        except IOError:
            with open(os.path.join(sys.path[0],'stat.json'),'w') as data_file:
                json.dump({},data_file)

        data['emergency_type']='e?'
        


        try:
            with open(os.path.join(sys.path[0],'stat.json'),'w') as data_file:
                json.dump(data,data_file)
        except Exception as e:
            print 'err',e
except KeyboardInterrupt:
    ser.close()
