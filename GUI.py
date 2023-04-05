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

qC = deque(maxlen = 100) #queue data structure
qV = deque(maxlen = 100)
qxc = deque(maxlen = 100)
qxv = deque(maxlen = 100)


tempc = 0 # temporary variable for current
xc = [] # x-axis for current
yc = [] # y-axis for current
current = 0

tempv = 0 # temporary variable for voltage
xv = [] # x-axis for voltage
yv = [] # y-axis for voltage
voltage = 0

i = 0  # counter
ser = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=1) # Establish the connection to the port used to sense current

# Current graph
fig1 = Figure(figsize=(12,10), dpi=50)
fig2 = Figure(figsize=(12,10), dpi=50)
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
       
        # creating container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
       
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
       
        # initialise frames
        self.frames = {}
       
        # iterate through a tuple with different pages
        for F in (StartPage, Page1, Page2, Graph):
           
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
           
        # placing the grid
        label.pack(padx = 10, pady = 10)
           
        button1 = ttk.Button(self, text = "Page 1", command = lambda : controller.show_frame(Page1))
           
        # placing the grid
        button1.pack()
           
        # button for page 2
        button2 = ttk.Button(self, text = "Page 2", command = lambda : controller.show_frame(Page2))
           
        # placing button2
        button2.pack()
       
        # button for page 3
        button3 = ttk.Button(self, text = "Graph",
                             command= lambda: controller.show_frame(Graph))
        # placing button3
        button3.pack()

# second window frame page1
class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
        label.pack(padx = 10, pady = 10)
 
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place
        # by using grid
        button1.pack()
 
        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text ="Page 2",
                            command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        button2.pack()

 
# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
        label.pack(padx = 10, pady = 10)
 
        # button to show page 1 with text
        # layout2
        button1 = ttk.Button(self, text ="Page 1",
                            command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.pack()
 
        # button to show start page with text
        # layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        button2.pack()
       
class Graph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "Graph", font = LARGEFONT)
        label.pack(pady = 10, padx = 10)
       
        # button to show start page with text
        button1 = ttk.Button(self, text="Home",
                             command= lambda : controller.show_frame(StartPage))
        # putting the button in its place by
        # using grid
        button1.pack()

        # For the first graph
        canvas_1 = FigureCanvasTkAgg(fig1, self)
        canvas_1.draw()
        canvas_1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
       
        toolbar = NavigationToolbar2Tk(canvas_1, self)
        toolbar.update()
        canvas_1._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

   
        # For the second graph
        canvas_2 = FigureCanvasTkAgg(fig2, self)
        canvas_2.draw()
        canvas_2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas_2, self)
        toolbar.update()
        canvas_2._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        
        
       
       
       
     
# Driver code
app = displayApp()
ani1 = animation.FuncAnimation(fig1, animate, interval=1, frames = 200, repeat = False)
ani2 = animation.FuncAnimation(fig2, animate, interval=1, frames = 200, repeat = False)
app.mainloop()
