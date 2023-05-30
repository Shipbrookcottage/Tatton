import tkinter as tk
import tkinter.messagebox
from tkdial import Meter
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import style
from matplotlib.figure import Figure
import matplotlib.animation as animation
import serial
import time
import os
from matplotlib import style
import threading
import csv
from datetime import date

import upload_blank

global filepath
filepath = 'data.csv'

def pause():
    os.system('arduino-cli compile -b arduino:avr:mega /Users/tadiwadzvoti/Documents/"4th Year Project"/Code/Arduino/Blank -u -p /dev/cu.usbmodem1301')

LARGEFONT = ("Verdana", 35)
style.use('fivethirtyeight')
        
                

class GUI(tk.Tk):
    """ class to set up GUI """
    # __init__ function for class in displayApp
    def __init__(self, *args, **kwargs):
       
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry('10000x9000')
        
        self.title('Demo')
       
        # creating container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
       
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
       
        # initialise frames
        self.frames = {}
       
        # iterate through a tuple with different pages
        for F in (Home, CompMode,GraphPage, Leaderboard, Grid):
           
            frame = F(container, self)
           
            # initialising frame of object
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame(Home)
   
    # to display the current frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
   
    # Start Page setup
    
class graph(tk.Canvas):
    def __init__(self, parent, title = '', ylabel = '', xlabel = '', label = '', ylim = 1, color = 'c',**kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.data = []
        self.ylim = ylim
        self.color = color
        self.label = label
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.fig = Figure(figsize=(11,7.5),dpi=50)
        self.plot = self.fig.add_subplot(1,1,1)
        self.plot.set_title(title)
        self.plot.set_ylabel(ylabel)
        self.plot.set_xlabel(xlabel)
        self.plot.set_ylim(0, ylim)
        self.line, = self.plot.plot([], [], color, marker = ',',label = label)
        self.plot.legend(loc='upper left') 
        
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack()
        
        self.ani = animation.FuncAnimation(self.fig, self.update_graph, interval = 200, frames = 200, repeat = False)
        self.canvas.draw()
        
    def update_graph(self, i):
        if self.data:
            self.line.set_data(range(len(self.data)), self.data)
            self.plot.set_xlim(0, len(self.data))
            
    def set(self, value):
        self.data.append(value)
        #self.label_data.config(text=value)
    
    def clear(self):
        self.data = []
        self.plot.clear()  # Clear the plot
        self.plot.set_ylim(0, self.ylim)  # Reset the y-axis limits
        self.plot.set_title(self.title)  # Reapply the title
        self.plot.set_xlabel(self.xlabel)  # Reapply the xlabel
        self.plot.set_ylabel(self.ylabel)  # Reapply the ylabel
        self.line, = self.plot.plot([], [], self.color, marker=',', label=self.line.get_label())
        self.plot.legend(loc='upper left')
        self.canvas.draw()
        
        # Stop and restart the animation
        self.canvas.get_tk_widget().after_cancel(self.ani)
        self.ani = animation.FuncAnimation(self.fig, self.update_graph, interval=200, frames=200, repeat=False)
        self.canvas.draw()
        
class EnergyLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)
        self.label_energy = tk.Label(self, font='Verdana 20')
        self.label_energy.pack()
    
    def setE(self, value):
        self.label_energy.config(text=value)
    
    def show(self):
        self.place(x=1040, y=630)  
    
    def hide(self):
        self.place_forget()
        

class Label_Frame(tk.LabelFrame) :
    def __init__(self, parent, title = '', value = 1, **kwargs):
        tk.LabelFrame.__init__(self, parent, **kwargs)
        self.frame = tk.LabelFrame(self, text = title)
        self.frame.pack()
        self.text = tk.Label(self.frame, text = value)
        self.text.pack()
        
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(Home,  self).__init__(parent)
        
        welcome = tk.Label(self, text='Welcome!', font ='Verdana 30').pack()
        
        button = tk.Button(self, text='Competition Mode', command= lambda : controller.show_frame(CompMode)).pack()
        
        button2 = tk.Button(self, text='Grid Mode', command= lambda : controller.show_frame(Grid)).pack()
        
class CompMode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(CompMode,  self).__init__(parent)
        
        welcome = tk.Label(self, text='Welcome to the Competition Mode!', font ='Verdana 30').pack() 
        usernameLabel = tk.Label(self, text="User Name").pack()
        global username
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=username).pack()
        
        def onClick():
            tkinter.messagebox.showinfo('Demo', 'Username Saved!')
            
        button = tk.Button(self, text='Enter', command = onClick).pack()
        button2 = tk.Button(self, text = 'Start Competition Mode', command  = lambda : controller.show_frame(GraphPage)).pack()
           
        
          

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(GraphPage, self).__init__(parent)

        # For the current graph
        current_canvas = graph(self, title='Current Graph', ylabel='Current (A)', xlabel='Time (s)', label='Current (A)', ylim = 40, color='c')
        current_canvas.place(x=10, y=50)
        #current_canvas.pack(expand=True, side=tk.LEFT)
        
        # For the voltage graph
        voltage_canvas = graph(self, title='Voltage Graph', ylabel='Voltage (V)', xlabel='Time (s)', label='Voltage (V)', ylim = 100, color='g')
        voltage_canvas.place(x=10, y=450)
        #voltage_canvas.pack(expand=True, side=tk.TOP)
        
        # For the power graph
        power_canvas = graph(self, title='Power Graph', ylabel='Power (W)', xlabel='Time (s)', label='Power (W)', ylim = 1000, color='b')
        power_canvas.place(x=600, y=50)
        #power_canvas.pack(expand=True, side=tk.LEFT)
        
        energy_frame = tk.LabelFrame(self, text='Cumulative Energy (J)', height= 100, width=150).place(x=1000, y=600)
        
        energy = EnergyLabel(energy_frame)
        energy.place(x=1040, y=630)         # energy_frames x+40 and y+30 from trial and error
        
        timer_frame = tk.LabelFrame(self, text='Remaining Time (s)', height = 100, width = 140).place(x=1200, y=100)
        
        timer_label = tk.Label(self ,timer_frame, text='Old Text', font='Verdana 20')
        timer_label.place(x=1260, y=130)         # timer_framee x+60 and y+30 from trial and error
        
        speed = Meter(self, radius=260, start=0, end=30, border_width=0,
               fg="black", text_color="white", start_angle=270, end_angle=-270,
               text_font="DS-Digital 30", scale_color="white", needle_color="red")
        
        speed.place(x=600, y = 500)
        
        def get_data():
            os.system('arduino-cli compile -b arduino:avr:mega /Users/tadiwadzvoti/Documents/"4th Year Project"/Code/Arduino/V_C -u -p /dev/cu.usbmodem1301')
            ser = serial.Serial('/dev/cu.usbmodem1301', 9600)
            global max_power
            global cum_energy # variable to store cumulative energy for the leaderboard
            max_power = 0
            while True:
                try:
                    pulldata = ser.readline()
                    string = pulldata.decode()
                    stripped_string = string.strip()
                    get_data = stripped_string.split(',')
                    current_canvas.set(float(get_data[0])) #current
                    voltage_canvas.set(float(get_data[1])) #voltage
                    power_canvas.set(float(get_data[2])) #power 
                    energy.setE(int(round(float(get_data[3])))) #energy
                    speed.set(float(get_data[4]))
                    if(max_power < float(get_data[2])):
                        max_power = float(get_data[2])
                    cum_energy = int(round(float(get_data[3])))
                except ValueError:
                    pause
                    data = [username.get(), max_power, cum_energy, date.today()]
                    write_csv(filepath, data)
                    break
                
        def start():  
            speed.set(0)
            energy.setE(0)
            energy.show()
            t = threading.Thread(target=get_data)      
            t.start()
        
        def deletetext():
            clear_graphs()
            energy.hide()
            pause
            controller.show_frame(Leaderboard)
        
        def write_csv(file, data_row):
            with open(file, 'a', newline='') as csv_file:
                write = csv.writer(csv_file)
                write.writerow(data_row)
        
        def clear_graphs():
            current_canvas.clear()
            voltage_canvas.clear()
            power_canvas.clear()
        
        
        button1 = tk.Button(self, text="Start", command = start).place(x=1300, y=700)
        
        button2 = tk.Button(self, text="Next", command = deletetext).place(x=1300, y=750)
        
        button3 = tk.Button(self, text = "Quit", command = quit).place(x=1300, y=800)
        
class Leaderboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(Leaderboard, self).__init__(parent)
        
        leaderboard_data = []
      
        leaderboard = tk.Listbox(self, width = 40, height = 10)
        leaderboard.pack()    
           
        def update_board():
            leaderboard.delete(0, tk.END)
            leaderboard_data.clear()
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                for i in reader:
                    if i != '':
                        if i[3] == str(date.today()):
                            leaderboard_data.append(i)
            leaderboard_data.sort(key = lambda max_p: max_p[1], reverse = True)
        
            for rank, row in enumerate(leaderboard_data, start=1):
                leaderboard.insert(tk.END, f"{rank}. {row[0]} - Maximum Power: {row[1]}")
            leaderboard.update()
        
        
        def up_lb():
            t_lb = threading.Thread(target=update_board)
            t_lb.start()
             
        update_leaderboard = tk.Button(self, text = 'Update', command = up_lb).pack()
        back_to_comp = tk.Button(self, text = 'Competition Mode', command = lambda : controller.show_frame(CompMode)).pack()
        button3 = tk.Button(self, text = "Quit", command = quit).place(x=1300, y=800)
        jelly = tk.Label(self, text = 'ADD FOOD EQUIVALENT', font = 'Verdana 30').pack()

# Need to write arduino code for Grid model mode first!!!!
class Grid(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(Grid, self).__init__(parent)
    
       # Wind = tk.LabelFrame(self, text = 'Wind Generation (W)').pack()
       # Wind_p = tk.Label(Wind, text = '10.4 W').pack()
        
       # Solar = tk.LabelFrame(self, text = 'Solar Generation').pack()
       # Solar_p = tk.Label(Solar, text = '7.4 W').pack()
        
        
        
    
# Driver code
app = GUI()
app.mainloop()
 
