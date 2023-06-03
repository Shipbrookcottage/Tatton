## @file
# @brief This file contains a Python code that utilizes the tkinter and matplotlib libraries to create a GUI application.
#
# The code creates a GUI application with several pages, including a home page, competitive mode page, graph page, leaderboard page, and grid page.
# Each page is represented by a class that inherits from the tkinter Frame class.
# The code also includes a Graph class that extends the tkinter Canvas widget to display a graph using matplotlib.
# Additional modules and libraries are imported to support various functionalities of the application.
#
# This code is a part of a larger project for the 4th year project.
#
# @note This code assumes that the required libraries and modules are installed.
# @note The code may require modification to work properly in different environments.
#

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

import upload_difficulty

## @var filepath
# Global variable that represents the file path for the data.csv file.
global filepath
filepath = 'data.csv'

## @brief Function to pause the execution of the program.
def pause():
    os.system('arduino-cli compile -b arduino:avr:mega /Users/tadiwadzvoti/Documents/4th_Year_Project/Code/Arduino/Difficulty -u -p /dev/cu.usbmodem1301')

## @var LARGEFONT
# Variable that represents the font style for large text.
LARGEFONT = ("Verdana", 35)

## @var style
# Variable that represents the style used by matplotlib for plotting.
style.use('fivethirtyeight')
        
                

class GUI(tk.Tk):
    """ class to set up GUI """
    # __init__ function for class in displayApp
    def __init__(self, *args, **kwargs):
       
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title('Demo')
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
       
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


## @class graph
# @brief A custom graph widget that extends the tkinter Canvas widget.
#
# The graph class provides functionality to create and update a graph using the matplotlib library.
# It allows customization of the graph's title, ylabel, xlabel, label, ylim, and color.

class graph(tk.Canvas):
    ## @brief Initializes a graph object.
    # @param parent The parent tkinter widget for the graph.
    # @param title The title of the graph.
    # @param ylabel The label for the y-axis.
    # @param xlabel The label for the x-axis.
    # @param label The label for the graph line.
    # @param ylim The upper limit for the y-axis.
    # @param color The color of the graph line.
    # @param **kwargs Additional keyword arguments for the tkinter Canvas widget.
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
    
    ## @brief Updates the graph with new data.
    # @param i The current iteration/frame number (not used in this implementation).    
    def update_graph(self, i):
        if self.data:
            self.line.set_data(range(len(self.data)), self.data)
            self.plot.set_xlim(0, len(self.data))
            self.plot.set_ylim(0, 1.25 * max(self.data))
    
    ## @brief Sets a new data value for the graph.
    # @param value The new data value.        
    def set(self, value):
        self.data.append(value)
          
    ## @brief Clears the graph and resets its properties.
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


## @class EnergyLabel
# @brief A custom energy label widget that extends the tkinter Label widget.
#
# The EnergyLabel class provides functionality to display an energy value using a tkinter Label.
# It allows setting the energy value and showing/hiding the label.   
class EnergyLabel(tk.Label):
    ## @brief Initializes an EnergyLabel object.
    # @param parent The parent tkinter widget for the energy label.
    # @param **kwargs Additional keyword arguments for the tkinter Label widget.
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)
        self.label_energy = tk.Label(self, font='Verdana 20')
        self.label_energy.pack()
    
    ## @brief Sets the energy value to be displayed.
    # @param value The energy value.
    def setE(self, value):
        self.label_energy.config(text=value)
        
    ## @brief Shows the energy label.
    def show(self):
        self.place(relx=0.72, rely=0.7)  
    
    ## @brief Hides the energy label.
    def hide(self):
        self.place_forget()
        
## @class Label_Frame
# @brief A custom label frame widget that extends the tkinter LabelFrame widget.
#
# The Label_Frame class provides functionality to create a labeled frame using the tkinter LabelFrame widget.
# It allows setting the title and value to be displayed within the frame.
# The class inherits from the tkinter LabelFrame class.
class Label_Frame(tk.LabelFrame):
    ## @brief Initializes a Label_Frame object.
    # @param parent The parent tkinter widget for the label frame.
    # @param title The title to be displayed on the frame.
    # @param value The value to be displayed within the frame.
    # @param **kwargs Additional keyword arguments for the tkinter LabelFrame widget.
    def __init__(self, parent, title = '', value = 1, **kwargs):
        tk.LabelFrame.__init__(self, parent, **kwargs)
        self.frame = tk.LabelFrame(self, text = title)
        self.frame.pack()
        self.text = tk.Label(self.frame, text = value)
        self.text.pack()

## @class Home
# @brief A custom frame widget for the home screen.
#
# The Home class provides functionality to create a home screen using the tkinter Frame widget.
# It displays a welcome message and buttons for different modes.
# The class inherits from the tkinter Frame class.        
class Home(tk.Frame):
    ## @brief Initializes a Home object.
    # @param parent The parent tkinter widget for the home screen.
    # @param controller The controller object for managing frame transitions.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(Home,  self).__init__(parent)
        
        welcome = tk.Label(self, text='Welcome!', font='Verdana 30', fg='blue')
        welcome.place(relx=0.5, rely=0.3, anchor='center')

        button = tk.Button(self, text='Competition Mode', command=lambda: controller.show_frame(CompMode), font='Arial 12 bold')
        button.place(relx=0.5, rely=0.5, anchor='center')

        button2 = tk.Button(self, text='Grid Mode', command=lambda: controller.show_frame(Grid), font='Arial 12 bold')
        button2.place(relx=0.5, rely=0.6, anchor='center')

## @class CompMode
# @brief A custom frame widget for the competition mode screen.
#
# The CompMode class provides functionality to create a competition mode screen using the tkinter Frame widget.
# It displays a welcome message, username input field, and buttons for entering and starting the competition mode.
# The class inherits from the tkinter Frame class.        
class CompMode(tk.Frame):
    ## @brief Initializes a CompMode object.
    # @param parent The parent tkinter widget for the competition mode screen.
    # @param controller The controller object for managing frame transitions.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(CompMode,  self).__init__(parent)
        
        welcome = tk.Label(self, text='Welcome to the Competition Mode!', font='Verdana 30', fg='blue')
        welcome.place(relx=0.5, rely=0.3, anchor='center')
        
        usernameLabel = tk.Label(self, text="User Name", font='Verdana 12 bold', fg='black')
        usernameLabel.place(relx=0.5, rely=0.4, anchor='center')
        
        global username
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=username, font='Verdana 12')
        usernameEntry.place(relx=0.5, rely=0.45, anchor='center')
        
        def onClick():
            tkinter.messagebox.showinfo('Demo', 'Username Saved!')
            
        button = tk.Button(self, text='Enter', command=onClick, font='Verdana 12', bg='lightblue', fg='black')
        button.place(relx=0.5, rely=0.5, anchor='center')
        
        button2 = tk.Button(self, text='Start Competition Mode', command=lambda: controller.show_frame(GraphPage),
                            font='Verdana 12 bold', bg='green', fg='white')
        button2.place(relx=0.5, rely=0.6, anchor='center')
           
## @class GraphPage
# @brief A custom frame widget for the graph page.
#
# The GraphPage class provides functionality to create a graph page using the tkinter Frame widget.
# It displays multiple graphs, energy label, countdown timer, and buttons for controlling the page.
# The class inherits from the tkinter Frame class.
class GraphPage(tk.Frame):
    ## @brief Initializes a GraphPage object.
    # @param parent The parent tkinter widget for the graph page.
    # @param controller The controller object for managing frame transitions.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        super(GraphPage, self).__init__(parent)
        
        self.count = 5
        self.time = 10
        
        

        # For the current graph
        current_canvas = graph(self, title='Current Graph', ylabel='Current (A)', xlabel='Time (s)', label='Current (A)', ylim = 3, color='c')
        current_canvas.place(relx=0.007, rely=0.056)
        #current_canvas.pack(expand=True, side=tk.LEFT)
        
        # For the voltage graph
        voltage_canvas = graph(self, title='Voltage Graph', ylabel='Voltage (V)', xlabel='Time (s)', label='Voltage (V)', ylim = 60, color='g')
        voltage_canvas.place(relx=0.007, rely=0.5)
        #voltage_canvas.pack(expand=True, side=tk.TOP)
        
        # For the power graph
        power_canvas = graph(self, title='Power Graph', ylabel='Power (W)', xlabel='Time (s)', label='Power (W)', ylim = 150, color='b')
        power_canvas.place(relx=0.417, rely=0.056)
        #power_canvas.pack(expand=True, side=tk.LEFT)
        
        energy_frame = tk.LabelFrame(self, text='Cumulative Energy (J)', height= 0.111, width=0.104).place(relx=0.694, rely=0.667)
        
        
        energy = EnergyLabel(energy_frame)
        energy.place(relx=0.722, rely=0.7)         # energy_frames x+40 and y+30 from trial and error
        
        timer_frame = tk.LabelFrame(self, text='Countdown (s)', height = 100, width = 140)
        timer_frame.place(relx=0.833, y=0.111)
        
        timer_label = tk.Label(timer_frame, text='5', font='Verdana 20')
        timer_label.place(relx = 0.045, y = 0.033)
        
        speed = Meter(self, radius=260, start=0, end=50, border_width=0,
               fg="black", text_color="white", start_angle=270, end_angle=-270,
               text_font="DS-Digital 30", scale_color="white", needle_color="red")
        
        speed.place(relx=0.417, rely = 0.556)
        
        def get_data():
            os.system('arduino-cli compile -b arduino:avr:mega /Users/tadiwadzvoti/Documents/4th_Year_Project/Code/Arduino/V_C -u -p /dev/cu.usbmodem1301')
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
        
        def countdown():
            if self.count > 0:
                self.count -= 1
                timer_label.config(text=str(self.count))
                self.after(1000, countdown)
            else:
                timer_frame.config(text = "Remaining Time (s)")
                t_timer = threading.Thread(target = timer)
                t_timer.start()
                
        
        def timer():
            if self.time > 0:
                self.time -= 1
                timer_label.config(text=str(self.time))
                self.after(1000, timer)
                
        def reset_timers():
            self.count = 5
            self.time = 10
            timer_frame.config(text = "Countdown (s)")
            timer_label.config(text = str(self.count))
                
                
        def start():  
            speed.set(0)
            energy.setE(0)
            energy.show()
            t = threading.Thread(target=get_data)  
            t_count = threading.Thread(target=countdown)    
            t.start()
            t_count.start()
            
        
        def deletetext():
            reset_timers()
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
        
        
        button1 = tk.Button(self, text="Start", command = start).place(relx=0.903, rely=0.778)
        
        button2 = tk.Button(self, text="Next", command = deletetext).place(relx=0.903, rely=0.833)
        
        button3 = tk.Button(self, text = "Quit", command = quit).place(relx=0.903, rely=0.889)

## @class Leaderboard
# @brief A custom frame widget for displaying a leaderboard.
#
# The Leaderboard class provides functionality to create a leaderboard using the tkinter Frame widget.
# It displays a list of ranked entries based on maximum power values.
# The class inherits from the tkinter Frame class.        
class Leaderboard(tk.Frame):
    ## @brief Initializes a Leaderboard object.
    # @param parent The parent tkinter widget for the leaderboard.
    # @param controller The controller object for managing frame transitions.
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

## @class Grid
# @brief A custom frame widget for displaying grid-related information.
#
# The Grid class provides functionality to create a grid mode view using the tkinter Frame widget.
# It displays information about wind and solar generation, and pedalling speed
# The class inherits from the tkinter Frame class.
class Grid(tk.Frame):
    ## @brief Initializes a Grid object.
    # @param parent The parent tkinter widget for the grid.
    # @param controller The controller object for managing frame transitions.
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
 
