#!/usr/bin/python
from upm import pyupm_i2clcd as lcd
from upm import pyupm_rfr359f as upmRfr359f
from upm import pyupm_grove as grove
from upm import pyupm_mq303a as upmMq303a
from upm import pyupm_buzzer as upmBuzzer
import time
import serial
import json
import os,sys
import threading

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
myAlcoholSensor = upmMq303a.MQ303A(0, 1)
button = grove.GroveButton(4)
warmed=False
space=' '*16
starttime=time.time()
btnstate=False
try:
    with open(os.path.join(sys.path[0],'stat.json')) as data_file:
        data = json.load(data_file)
except IOError:
    with open(os.path.join(sys.path[0],'stat.json'),'w') as data_file:
        json.dump({},data_file)

try:
    while 1:
        response = ser.readline()
        try:
            with open(os.path.join(sys.path[0],'stat.json'),'w') as data_file:
                print data
                json.dump(data,data_file)
        except Exception as e:
            print 'err',e
        try:
            with open(os.path.join(sys.path[0],'stat.json')) as data_file:
                data = json.load(data_file)
        except IOError:
            with open(os.path.join(sys.path[0],'stat.json'),'w') as data_file:
                json.dump({},data_file)

        res=response.split(';')
        print data
        print res
        if len(res)!=4:
            continue
        if int(float(res[2]))>50:
                ChangeDisplay1('red','HighTemp')
                data['emergency_type']='FIRE'
                continue
        if btnstate:
            if not button.value():
                ChangeDisplay1('red','Help')
                data['emergency_type']='HELP'
                continue
            else:
                btnstate=False
                data['emergency_type']=0
        else:
            if button.value():
                ChangeDisplay1('red','Help')
                data['emergency_type']='HELP'
                btnstate=True
                continue

        if ((time.time()-starttime)>120) and myAlcoholSensor.value()>200:
            data['emergency_type']='Danger'
            ChangeDisplay1('red','Danger')
        else:
            data['emergency_type']=0
            if (myDistInterrupter1.objectDetected() and myDistInterrupter2.objectDetected()):
                ChangeDisplay1('red','Full')
                print 'Full'
                data['isfull']=1
            else:
                data['isfull']=0
                if res[0]=='True':
                    print 't'
                    ChangeDisplay1('yellow','trash out')
                else:
                    print 'f'
                    ChangeDisplay1('green','OK')
                ChangeDisplay2('temp='+str(int(float(res[2])))+' '+'humi='+str(int(float(res[3]))))
        data['flowrate']=int(res[1])
        data['temp']=int(float(res[2]))
        data['humi']=int(float(res[3]))

except KeyboardInterrupt:
    ser.close()
