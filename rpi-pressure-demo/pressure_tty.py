import os
import pty
from time import sleep

import serial

master, slave = pty.openpty()
s_name = os.ttyname(slave)

ser = serial.Serial(s_name)
print('Bound to', s_name)

while True:
    os.write(master, 'DEBUG: nobody expects the spanish inquisition\n'.encode())
    for rep in range(10):
        sleep(1)
        vals = ','.join([str(i*rep) for i in range(8)]) + '\n'
        os.write(master, vals.encode())
