from tkinter import *
import tkinter as tk # proper way to import tkinter
import serial
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use("fivethirtyeight")
import threading
import upload 
upload

class Graph(tk.Frame):
    def __init__(self, master=None, title='', ylabel='', label='', color='c', ylim=1, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.data = []
        fig = Figure(figsize = (7, 6))
        self.plot = fig.add_subplot(1,1,1)
        self.plot.set_title(title)
        self.plot.set_ylabel(ylabel)
        self.plot.set_ylim(0, ylim)
        self.line, = self.plot.plot([], [], color, marker = 'o',label = label)
        self.plot.legend(loc='upper left')
        
        label = Label(self, text = ylabel, relief = "solid", font = "Times 22 bold").grid(row = 0, column = 3)
        button_1 = Button(self, text = "Back To Homepage", command = F1.tkraise).grid(row = 1, column = 2)
        label_1 = Label(self, text = "Current Value: ", relief = "solid", font = "Verdana 10 bold").grid(row = 2, column = 2)
        self.label_data = Label(self, font = "Verdana 10")
        self.label_data.grid(row = 2, column = 3)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row = 3, column = 3)
        
        ani = animation.FuncAnimation(fig, self.update_graph, interval = 200, frames = 60, repeat = False)
        canvas.draw()
        
    def update_graph(self, i):
        if self.data:
            self.line.set_data(range(len(self.data)), self.data)
            self.plot.set_xlim(0, len(self.data))
    
    def set(self, value):
        self.data.append(value)
        self.label_data.config(text=value)
        
my_window = Tk()
my_window.title("Graphical User Interface Try #1")
my_window.geometry("720x720")

F1 = Frame(my_window, relief = RAISED)
F2 = Graph(my_window, title='Current Graph', ylabel='Temperature', color='c', label='Current (A)', ylim = 40, relief = RAISED)
F3 = Graph(my_window, title='Voltage Graph', ylabel='Humidity', color='g', label='Voltage (V)', ylim = 500, relief = RAISED)
F4 = Graph(my_window, title='Power Graph', ylabel='Water Volume', color='b', label='Power (W)', ylim = 6000, relief = RAISED)    

#For Frame One
label_1 = Label(F1, text = "Homepage of GUI", relief = "solid", font = "Times 22 bold")
label_1.grid(row = 0, column = 3)
button_1 = Button(F1, text = "Page of Humidity", relief = GROOVE, bd = 8, command = F2.tkraise)
button_1.grid(row = 1, column = 2)
button_2 = Button(F1, text = "Page of Temperature", relief = GROOVE, bd = 8, command = F3.tkraise)
button_2.grid(row = 1, column = 3)
button_3 = Button(F1, text = "Page of Water", relief = GROOVE, bd = 8, command = F4.tkraise)
button_3.grid(row = 1, column = 4)

for frame in(F1, F2, F3, F4):
    frame.grid(row = 0, column = 0, sticky = "NSEW")

F1.tkraise()

def get_data():
    ser = serial.Serial('/dev/cu.usbmodem1301', 9600)
    while True:
        pulldata = ser.readline()
        string = pulldata.decode()
        stripped_string = string.strip()
        get_data = stripped_string.split(',')
        F2.set(float(get_data[0])) #current
        F3.set(float(get_data[1])) #voltage
        F4.set(float(get_data[2])) #power

t = threading.Thread(target=get_data)
t.daemon = True
t.start()

my_window.mainloop()
