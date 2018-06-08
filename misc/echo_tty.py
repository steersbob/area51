import os
import pty
import serial

master, slave = pty.openpty()
s_name = os.ttyname(slave)

ser = serial.Serial(s_name)
print('Bound to', s_name)

# To read from the device
while True:
    recv = os.read(master, 1000)
    # echoes empty OneWireTempSensor
    repl = f'{recv.decode().rstrip()}|00060000\n'.encode()
    print(repl)
    os.write(master, repl)
