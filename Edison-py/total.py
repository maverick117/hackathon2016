#!/usr/bin/python
from upm import pyupm_i2clcd as lcd
import time
import serial

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
    else :
        myLcd.clear()
        myLcd.setColor(255, 0, 0)
        myLcd.write('Error'+space)
        
def ChangeDisplay2(_text):
    myLcd.setCursor(1,0)
    myLcd.write(_text+space)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.setCursor(0,0)
space=' '*16

#ser.write("testing")
try:
    while 1:
        response = ser.readline()
        if ';' not in response:
            continue
        res=response.split(';')
        print res
        if res[0]=='True':
            print 't'
            ChangeDisplay1('yellow','trash out')
        else:
            print 'f'
            ChangeDisplay1('green','OK')
        ChangeDisplay2('Flowrate='+str(int(res[1])))
except KeyboardInterrupt:
     ser.close()
