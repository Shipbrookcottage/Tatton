import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import sys
import matplotlib.animation as animation
from matplotlib import style
from queue import Queue
from collections import deque
import upload

upload


qC = deque(maxlen = 100) #queue data structure
qV = deque(maxlen = 100)
qxc = deque(maxlen = 100)
qvc = deque(maxlen = 100)
tempc = 0 # temporary variable for current
xc = [] # x-axis for current
yc = [] # y-axis for current
current = 0
i = 0  # counter

tempv = 0 # temporary variable for voltage
xv = [] # x-axis for voltage
yv = [] # y-axis for voltage
voltage = 0
ser = serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=1) # Establish the connection to the port used to sense current

style.use('fivethirtyeight')

fig1 = plt.figure("Current Plot")
fig2 = plt.figure("Voltage Plot")
ac = fig1.add_subplot(1,1,1)
av = fig2.add_subplot(1,1,1)

def animate(i):
    line = ser.readline()
   
    if line:
        string = line.decode()
        stripped_string = string.strip()
        if len(stripped_string) > 0:
            if stripped_string[0] == 'C':
                try:
                    current = float(stripped_string[1:])
                    if current < 0:
                        current = 0
                except ValueError:
                    current = tempc
                qxc.append(i)
                xc.append(i)
                qC.append(current)
                yc.append(current)
                tempc = current
                ac.clear()
                ac.plot(qxc,qC)
                #qxc.popleft()
                #qC.popleft()
            elif stripped_string[0] == 'V':
                try:
                    voltage = float(stripped_string[1:])
                    if voltage < 10:
                        voltage = 0
                except ValueError:
                    voltage = tempv
                qvc.append(i)
                qV.append(voltage)
                yv.append(voltage)
                tempv = voltage
                i += 0.2
                av.clear()
                av.plot(qvc, qV)

               

ani1 = animation.FuncAnimation(fig1, animate, interval=1, frames = 10, repeat = False)
ani2 = animation.FuncAnimation(fig2,animate,interval =1,frames = 10, repeat = False)
plt.show()
