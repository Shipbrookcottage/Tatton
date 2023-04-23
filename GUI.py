import tkinter as tk
import matplotlib
import urllib
import json
import random
import time
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import style
from matplotlib.figure import Figure
import matplotlib.animation as animation
import serial
import numpy as np
import sys
from matplotlib import style
from collections import deque
import upload # script that uploads code to the arduino

upload

LARGEFONT = ("Verdana", 35)
style.use('fivethirtyeight')
ser = serial.Serial('/dev/cu.usbmodem1301', 9600, timeout=1) # Establish the connection to the port used to sense current

qC = deque(maxlen = 200) #queue data structure
qV = deque(maxlen = 200)
qP = deque(maxlen = 200)
qxc = deque(maxlen = 200)
qxv = deque(maxlen = 200)
qxp = deque(maxlen = 200)
tempc = 0 # temporary variable for current
xc = [] # x-axis for current
yc = [] # y-axis for current
current = 0

tempv = 0 # temporary variable for voltage
xv = [] # x-axis for voltage
yv = [] # y-axis for voltage
voltage = 0

tempp = 0
xp = []
yp = []
power = 0

i = 0  # counter
fig1 = Figure(dpi=50)
fig2 = Figure(dpi=50)
fig3 = Figure(dpi=50)
ac = fig1.add_subplot(1,1,1)
av = fig2.add_subplot(1,1,1)
ap = fig3.add_subplot(1,1,1)

fc = Figure(dpi=50)
f_ac = fc.add_subplot(1,1,1)


def animate(i):
    line = ser.readline()
    
    if start:
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
                    #i += 0.2
                    ac.clear()
                    ac.plot(qxc, qC)
                    ac.set_xlabel('Time (s)', fontsize=25)
                    ac.set_ylabel('Current (A)', fontsize=25)
                    ac.set_title('Current Plot', fontsize=30)
                if stripped_string[0] == 'V':
                    try:
                        voltage = float(stripped_string[1:])
                        if voltage < 10:
                            voltage = 0
                    except ValueError:
                        voltage = tempv
                    qxv.append(i)
                    xv.append(i)
                    qV.append(voltage)
                    yv.append(voltage)
                    tempv = voltage
                    #i += 0.2
                    av.clear()
                    av.plot(qxv, qV)
                    av.set_xlabel('Time (s)', fontsize=25)
                    av.set_ylabel('Voltage (V)', fontsize=25)
                    av.set_title('Voltage Plot', fontsize=30)
                if stripped_string[0] == 'P':
                    try:
                        power = float(stripped_string[1:])
                        if power < 10:
                            power = 0
                    except ValueError:
                        power = tempp
                    qxp.append(i)
                    xp.append(i)
                    qP.append(power)
                    yp.append(power)
                    tempp = power
                    #i += 0.2
                    ap.clear()
                    ap.plot(qxp, qP)
                    ap.set_xlabel('Time (s)', fontsize=25)
                    ap.set_ylabel('Power (P)', fontsize=25)
                    ap.set_title('Power Plot', fontsize=30)
                

class displayApp(tk.Tk):
    """ class to set up GUI """
    # __init__ function for class in displayApp
    def __init__(self, *args, **kwargs):
       
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.attributes('-fullscreen', True)
       
        # creating container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
       
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
       
        # initialise frames
        self.frames = {}
       
        # iterate through a tuple with different pages
        for F in (Graph, Final):
           
            frame = F(container, self)
           
            # initialising frame of object
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame(Graph)
   
    # to display the current frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
   
    # Start Page setup
           

class Graph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # For the current graph
        canvas_1 = FigureCanvasTkAgg(fig1, self)
        canvas_1.draw()
        canvas_1.get_tk_widget().place(x=10, y=-350, width=400, height=450)
       
        #toolbar1 = NavigationToolbar2Tk(canvas_1, self)
        #toolbar1.update()
        canvas_1._tkcanvas.place(x=10, y=80, width=400)

   
        # For the voltage graph
        canvas_2 = FigureCanvasTkAgg(fig2, self)
        canvas_2.draw()
        canvas_2.get_tk_widget().place(x=410, y=-350, width=500, height=450)
        
        #toolbar2 = NavigationToolbar2Tk(canvas_2, self)
        #toolbar2.update()
        canvas_2._tkcanvas.place(x=460, y=80, width=500)
        
        # For the power graph
        canvas_3 = FigureCanvasTkAgg(fig3, self)
        canvas_3.draw()
        canvas_3.get_tk_widget().place(x=10, y=-350, width=400, height=450)
        
        #toolbar3 = NavigationToolbar2Tk(canvas_3, self)
        #toolbar3.update()
        canvas_3._tkcanvas.place(x=990, y=80, width=400)
        
        
        
        label = ttk.Label(self, text = "Graph", font = LARGEFONT).pack()
        
        button2 = ttk.Button(self, text = "Quit", command = quit).place(x=1300, y=800)
        
        button3 = ttk.Button(self, text="Start", command = start_animation).pack()
        
        button4 = ttk.Button(self, text="Next", command = lambda : controller.show_frame(Final)).place(x=1300, y=700)
        
class Final(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        button = ttk.Button(self, text="Plot", command = plot).pack()
        
        
        canvas = FigureCanvasTkAgg(fc, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
        
start = False
def start_animation():
    global start
    start ^= True
    i = 0
    frames = 0

def plot():
    f_ac.plot(xc, yc)        
# Driver code
app = displayApp()
ani1 = animation.FuncAnimation(fig1, animate, interval=200, frames = 60, repeat = False, blit = False)
ani2 = animation.FuncAnimation(fig2, animate, interval=200, frames = 60, repeat = False, blit = False)
ani3 = animation.FuncAnimation(fig3, animate, interval=200, frames = 60, repeat = False, blit = False)
app.mainloop()
