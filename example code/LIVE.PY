import serial
import time
from matplotlib import pyplot as plt, animation

import csv



BAUD_RATE = 115200
SERIAL_PORT="COM4"

ser = serial.Serial('COM4', 115200)
time.sleep(2)
x=[]
sensorData =[]

def read_and_process_data():
    line=ser.readline().decode().strip()

    print(f'{line}, {type(line)}')

    
    #sensorValues= line.split(', ')
    #print(type(line))
    
    #x.append(float(sensorValues[0]))
    #print(x)
    #sensorData.append(float(sensorValues[1]))

    #print(f'Time: {sensorValues[0]}, Data: {sensorValues[1]}')

def update(frame):
    read_and_process_data()
    #plt.cla()
    #plt.plot(TM,sensorData,label="Data")
    #plt.xlabel("Time")
    #plt.ylabel("Sensor Values")
    #plt.legend()

#def on_close(event):
#    with open('arduino_data.csv', 'w', newline='') as csvfile:
#        writer = csv.writer(csvfile)
##        writer.writerow(['Time', 'DataValue'])
 #       for a, s1 in zip(x,sensorData):
 #           writer.writerow([a,s1])


#fig,ax=plt.subplots()
#fig.canvas.mpl_connect("close_event", on_close)


#anim = animation.FuncAnimation(fig, update,interval=10)

#plt.show()
while(1):
    read_and_process_data()

