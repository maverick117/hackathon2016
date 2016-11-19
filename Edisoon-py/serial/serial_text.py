import serial
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.write("testing")
try:
    while 1:
            response = ser.readline()
            if ';' not in response:
                continue
            res=response.split(';')
            needhelp=bool(res[0])
            flowrate=int(res[1])
            
except KeyboardInterrupt:
     ser.close()
