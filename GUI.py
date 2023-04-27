import tkinter as tk
import matplotlib
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import style
from matplotlib.figure import Figure
import matplotlib.animation as animation
import serial
import time
from matplotlib import style
import threading
import upload_blank
import upload_comp # script that uploads code to the arduino
#upload_blank
upload_comp

LARGEFONT = ("Verdana", 35)
style.use('fivethirtyeight')
        
                

class displayApp(tk.Tk):
    """ class to set up GUI """
    # __init__ function for class in displayApp
    def __init__(self, *args, **kwargs):
       
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry('1000x9000')
       
        # creating container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
       
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
       
        # initialise frames
        self.frames = {}
       
        # iterate through a tuple with different pages
        for F in (GraphPage, Grid):
           
            frame = F(container, self)
           
            # initialising frame of object
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame(GraphPage)
   
    # to display the current frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
   
    # Start Page setup
    
class graph(tk.Canvas):
    def __init__(self, parent, x_coord=1, y_coord=1, title='', ylabel='', xlabel='', label='', ylim=1, color='c',**kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.data = []
        fig = Figure(figsize=(11,7.5),dpi=50)
        self.plot = fig.add_subplot(1,1,1)
        self.plot.set_title(title)
        self.plot.set_ylabel(ylabel)
        self.plot.set_xlabel(xlabel)
        self.plot.set_ylim(0, ylim)
        self.line, = self.plot.plot([], [], color, marker = ',',label = label)
        self.plot.legend(loc='upper left')
        
        self.canvas = FigureCanvasTkAgg(fig, self)
        #self.canvas.get_tk_widget().place(x=x_coord, y=y_coord, width=50, height=50)
        self.canvas.get_tk_widget().pack()
        
        ani = animation.FuncAnimation(fig, self.update_graph, interval = 200, frames = 200, repeat = False)
        self.canvas.draw()
        
    def update_graph(self, i):
        if self.data:
            self.line.set_data(range(len(self.data)), self.data)
            self.plot.set_xlim(0, len(self.data))
            
    def set(self, value):
        self.data.append(value)
        #self.label_data.config(text=value)
        
class EnergyLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)
        self.label_energy = tk.Label(self, font='Verdana 20')
        self.label_energy.pack()
    
    def setE(self, value):
        self.label_energy.config(text=value)

class Label_Frame(tk.LabelFrame) :
    def __init__(self, parent, title = '', value = 1, **kwargs):
        tk.LabelFrame.__init__(self, parent, **kwargs)
        self.frame = tk.LabelFrame(self, text = title)
        self.frame.pack()
        self.text = tk.Label(self.frame, text = value)
        self.text.pack()
          

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(GraphPage, self).__init__(parent)

        # For the current graph
        current_canvas = graph(self, x_coord = 10, y_coord = 0, title='Current Graph', ylabel='Current (A)', xlabel='Time (s)', label='Current (A)', ylim = 40, color='c')
        current_canvas.place(x=10, y=50)
        #current_canvas.pack(expand=True, side=tk.LEFT)
        
        # For the voltage graph
        voltage_canvas = graph(self, x_coord = 410, y_coord = 0, title='Voltage Graph', ylabel='Voltage (V)', xlabel='Time (s)', label='Voltage (V)', ylim = 500, color='g')
        voltage_canvas.place(x=10, y=450)
        #voltage_canvas.pack(expand=True, side=tk.TOP)
        
        # For the power graph
        power_canvas = graph(self, x_coord = 910, y_coord = 0, title='Power Graph', ylabel='Power (W)', xlabel='Time (s)', label='Power (W)', ylim = 6000, color='b')
        power_canvas.place(x=600, y=50)
        #power_canvas.pack(expand=True, side=tk.LEFT)
        
        energy = EnergyLabel(self)
        energy.place(x=1300, y=600)
        
        def timer(seconds):
            
            seconds = seconds - 1
            timer_label.config(text=seconds)
            timer_label.after(1000, timer)
        
        def update():
            timer_label.config(text='New Text')
        
        timer_label = tk.Label(self, text='Old Text')
        timer_label.place(x=1300, y=400)
        
        
        

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
                energy.setE(int(round(float(get_data[3])))) #energy
                
                
                
        
        t = threading.Thread(target=get_data)
        t.daemon = True
        t.start()
        
        t_timer = threading.Thread(target=timer(10))
        t_timer.daemon = True
        t_timer.start()
        
        button1 = ttk.Button(self, text="Change", command=lambda: controller.show_frame(Grid)).place(x=1300, y=700) 
        
        
        button2 = ttk.Button(self, text = "Quit", command = quit).place(x=1300, y=800)
        
class Grid(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        Wind = tk.LabelFrame(self, text = 'Wind Generation (W)').pack()
        Wind_p = tk.Label(Wind, text = '10.4 W').pack()
        
        Solar = tk.LabelFrame(self, text = 'Solar Generation').pack()
        Solar_p = tk.Label(Solar, text = '7.4 W').pack()
        
        
        
    
# Driver code
app = displayApp()
app.mainloop()
