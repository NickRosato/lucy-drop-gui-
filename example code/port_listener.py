import serial as ser
import io
import numpy as np

# STATIC VARIABLES
BAUD_RATE = 115200
SERIAL_PORT = 'COM4'
BYTES_RECORDED = 2000

# setting up pyserial
ser = ser.Serial()
ser.baudrate = BAUD_RATE
ser.port = SERIAL_PORT

# sio needed if decoding while capturing data, sio wraps ser class
# sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), None, None, '\r\n')


# currently data captured in buffer is likely wrong, need to look into emptying buffer right before or after input statement

def collect_data():
  #input('Press ENTER when you are ready to collect data...')
  print('Ready...')##countdown
  ser.open()
  print('Start...')##greenlight
  recorded_buffer = ser.read(BYTES_RECORDED)
  # changes data from type byte to type string and removes EOL characters
  output = recorded_buffer.decode()
  newOutput = output.splitlines()
  newNewOutput=np.array(newOutput,dtype=np.float32)
  #output = recorded_buffer.decode()
  print('----------------------')
  print(newNewOutput)
  print('----------------------')

  print(type(newNewOutput))
  print('----------------------')

  print(type(newNewOutput[0]))
  print('----------------------')
  print(newNewOutput[0])
  #print(np.shape(newNewOutput))

collect_data()

ser.close()

