import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import sys
import matplotlib.animation as animation
from matplotlib import style

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

fig = plt.figure()
ac = fig.add_subplot(1,1,1)
av = fig.add_subplot(2,2,2)

def animate(i):
    line = ser.readline()
   
    if line:
        string = line.decode()
        stripped_string = string.strip()
        if len(stripped_string) > 0:
            if stripped_string[0] == 'C':
                try:
                    current = float(stripped_string[1:])
                except ValueError:
                    current = tempc
                xc.append(i)
                yc.append(current)
                tempc = current
                ac.clear()
                ac.plot(xc,yc)
            elif stripped_string[0] == 'V':
                try:
                    voltage = float(stripped_string[1:])
                except ValueError:
                    voltage = tempv
                xv.append(i)
                yv.append(voltage)
                tempv = voltage
                i += 0.2
                av.clear()
                av.plot(xv, yv)
               
               

ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()
