import serial
import io

# STATIC VARIABLES
BAUD_RATE = 9600
SERIAL_PORT = 'COM3'
BYTES_RECORDED = 1000

# setting up pyserial
ser = serial.Serial()
ser.baudrate = BAUD_RATE
ser.port = SERIAL_PORT

# sio needed if decoding while capturing data, sio wraps ser class
# sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), None, None, '\r\n')

# currently data captured in buffer is likely wrong, need to look into emptying buffer right before or after input statement
ser.open()
input('Press ENTER when you are ready to collect data...')
recorded_buffer = ser.read(BYTES_RECORDED)

# changes data from type byte to type string and removes EOL characters
output = recorded_buffer.decode()

print(output)

ser.close()
