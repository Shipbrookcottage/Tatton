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
import threading
import upload # script that uploads code to the arduino

upload

LARGEFONT = ("Verdana", 35)
style.use('fivethirtyeight')

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
        
                

class displayApp(tk.Tk):
    """ class to set up GUI """
    # __init__ function for class in displayApp
    def __init__(self, *args, **kwargs):
       
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry('720x720')
       
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
    
class graph(tk.Canvas):
    def __init__(self, parent, x_coord=1, y_coord=1, height=1, width=1, title='', ylabel='', xlabel='', label='', ylim=1, color='c',**kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.data = []
        fig = Figure(dpi=100)
        self.plot = fig.add_subplot(1,1,1)
        self.plot.set_title(title)
        self.plot.set_ylabel(ylabel)
        self.plot.set_xlabel(xlabel)
        self.plot.set_ylim(0, ylim)
        self.line, = self.plot.plot([], [], color, marker = ',',label = label)
        self.plot.legend(loc='upper left')
        
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        #self.canvas.get_tk_widget().place(x=x_coord, y=y_coord, width=width, height=height)
        self.canvas.get_tk_widget().pack()
        
        ani = animation.FuncAnimation(fig, self.update_graph, interval = 200, frames = 100, repeat = False)
        self.canvas.draw()
        
    def update_graph(self, i):
        if self.data:
            self.line.set_data(range(len(self.data)), self.data)
            self.plot.set_xlim(0, len(self.data))
            
    def set(self, value):
        self.data.append(value)
        #self.label_data.config(text=value)

     

class Graph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(Graph, self).__init__(parent)

        # For the current graph
        current_canvas = graph(self, x_coord = 10, y_coord = -350, width = 400, height = 450, title='Current Graph', ylabel='Current (A)', xlabel='Time (s)', label='Current (A)', ylim = 40, color='c')
        # For the voltage graph
        voltage_canvas = graph(self, x_coord = 410, y_coord = -350, width = 500, height = 450, title='Voltage Graph', ylabel='Voltage (V)', xlabel='Time (s)', label='Voltage (V)', ylim = 500, color='g')

        power_canvas = graph(self, x_coord = 960, y_coord = -350, width = 400, height = 450, title='Power Graph', ylabel='Power (W)', xlabel='Time (s)', label='Power (W)', ylim = 6000, color='b')
    

        def get_data():
            ser = serial.Serial('/dev/cu.usbmodem1301', 9600)
            while True:
                pulldata = ser.readline()
                string = pulldata.decode()
                stripped_string = string.strip()
                get_data = stripped_string.split(',')
                current_canvas.set(float(get_data[0])) #current
                voltage_canvas.set(float(get_data[1])) #voltage
                power_canvas.set(float(get_data[2])) #power 
        
        t = threading.Thread(target=get_data)
        t.daemon = True
        t.start()  
        
        
        label = ttk.Label(self, text = "Graph", font = LARGEFONT).pack()
        
        button2 = ttk.Button(self, text = "Quit", command = quit).place(x=1300, y=800)
        
class Final(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        canvas = FigureCanvasTkAgg(fc, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
    
# Driver code
app = displayApp()
app.mainloop()
