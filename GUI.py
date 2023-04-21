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
qC = deque(maxlen = 50) #queue data structure
qV = deque(maxlen = 50)
qxc = deque(maxlen = 50)
qxv = deque(maxlen = 50)
tempc = 0 # temporary variable for current
xc = [] # x-axis for current
yc = [] # y-axis for current
current = 0
tempv = 0 # temporary variable for voltage
xv = [] # x-axis for voltage
yv = [] # y-axis for voltage
voltage = 0
i = 0  # counter
# Current graph
fig1 = Figure(dpi=50)
fig2 = Figure(dpi=50)
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
                i += 0.2
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
                qV.append(voltage)
                yv.append(voltage)
                tempv = voltage
                i += 0.2
                av.clear()
                av.plot(qxv, qV)
                av.set_xlabel('Time (s)', fontsize=25)
                av.set_ylabel('Voltage (V)', fontsize=25)
                av.set_title('Voltage Plot', fontsize=30)
                

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
        for F in (StartPage, Graph):
           
            frame = F(container, self)
           
            # initialising frame of object
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame(StartPage)
   
    # to display the current frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
   
    # Start Page setup
   
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
       
        # label for the frame layout
        label = ttk.Label(self, text = "Home", font = LARGEFONT)
        
        button1 = ttk.Button(self, text="Graph", command = lambda: controller.show_frame(Graph)).pack()
           

class Graph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # For the first graph
        canvas_1 = FigureCanvasTkAgg(fig1, self)
        canvas_1.draw()
        canvas_1.get_tk_widget().place(x=10, y=-350, width=400, height=450)
       
        toolbar1 = NavigationToolbar2Tk(canvas_1, self)
        toolbar1.update()
        canvas_1._tkcanvas.place(x=10, y=80, width=400)

   
        # For the second graph
        canvas_2 = FigureCanvasTkAgg(fig2, self)
        canvas_2.draw()
        canvas_2.get_tk_widget().place(x=10, y=-350, width=500, height=450)
        
        toolbar2 = NavigationToolbar2Tk(canvas_2, self)
        toolbar2.update()
        canvas_2._tkcanvas.place(x=410, y=80, width=500)
        
        label = ttk.Label(self, text = "Graph", font = LARGEFONT).pack()
        
        button1 = ttk.Button(self, text="Home", command= lambda : controller.show_frame(StartPage)).pack()
        
        button2 = ttk.Button(self, text = "Quit", command = quit).place(x=1300, y=800)
        
       # button3 = ttk.Button(self, text="Start", command = lambda: graph).pack()


# Driver code
app = displayApp()
ani1 = animation.FuncAnimation(fig1, animate, interval=50, frames = 60, repeat = False)
ani2 = animation.FuncAnimation(fig2, animate, interval=50, frames = 60, repeat = False)
app.mainloop()
