from serial.tools import list_ports
import serial
import time
import csv

ports = list_ports.comports()
for port in ports: print(port)

f = open('data.csv','w',newline='')
f.truncate()

serialCom=serial.Serial('COM3',115200)
print("Flush")
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)
print("Start")
kmax=500
for k in range(kmax):
    try:
        s_bytes=serialCom.readline()
        decode_bytes = s_bytes.decode("utf-8").strip('\r\n')
        
        if k==0:
            values= decode_bytes.split(",")
        else:
            values = [float(x) for x in decode_bytes.split(",")]
        #print(values)

        writer = csv.writer(f,delimiter =',')
        writer.writerow(values)
    except:
        print("Error: Line was not recorded")

f.close()