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
from PIL import ImageTk, Image

os.system('arduino-cli compile -b arduino:avr:mega /Users/tadiwadzvoti/Documents/4th_Year_Project/Code/Arduino/Difficulty -u -p /dev/cu.usbmodem1301')

## @var filepath
# Global variable that represents the file path for the data.csv file.
global filepath
filepath = 'data.csv'

## @brief Function to pause the execution of the program.
def pause():
    os.system('arduino-cli compile -b arduino:avr:mega /Users/tadiwadzvoti/Documents/4th_Year_Project/Code/Arduino/Difficulty -u -p /dev/cu.usbmodem1301')

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
        for F in (Home, CompMode, GraphPage, Leaderboard, Grid):
           
            frame = F(container, self)
           
            # initialising frame of object
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame(Home)
   
    # to display the current frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
   

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
        display_width = self.winfo_screenwidth()  # Width of your display
        display_height = self.winfo_screenheight()  # Height of your display
        
        # Calculate scaling factors
        width_scale = display_width / 1440  # Adjust as needed
        height_scale = display_height / 900  # Adjust as needed
        
        # Calculate adjusted dimensions
        adjusted_width = 11 * width_scale
        adjusted_height = 7.5 * height_scale
        adjusted_dpi = 50 * min(width_scale, height_scale)
        
        self.data = []
        self.ylim = ylim
        self.color = color
        self.label = label
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.fig = Figure(figsize=(adjusted_width, adjusted_height),dpi=50)
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
            self.plot.set_xlim(0, (2*len(self.data)/7))
            #self.plot.set_ylim(0, max(self.data))
    
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
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        font_size = int(screen_height * (50/1440))
        self.label_energy = tk.Label(self, font = ('Verdana', font_size))
        self.label_energy.pack()
    
    ## @brief Sets the energy value to be displayed.
    # @param value The energy value.
    def setE(self, value):
        self.label_energy.config(text=value)
        
    ## @brief Shows the energy label.
    def show(self):
        self.place(relx=0.73, rely=0.7)  
    
    ## @brief Hides the energy label.
    def hide(self):
        self.place_forget()
        
class WindLabel(tk.Label):
    ## @brief Initializes an WindLabel object.
    # @param parent The parent tkinter widget for the wind label.
    # @param **kwargs Additional keyword arguments for the tkinter Label widget.
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        font_size = int(screen_height * (100/1440))
        
        self.label_wind = tk.Label(self, font = ('Verdana', font_size))
        self.label_wind.pack()
    
    ## @brief Sets the wind value to be displayed.
    # @param value The wind value.
    def setW(self, value):
        self.label_wind.config(text=value)
        
    ## @brief Shows the wind label.
    def show(self):
        self.place(relx=0.2, rely=0.5, anchor = 'center')  
    
    ## @brief Hides the wind label.
    def hide(self):
        self.place_forget()
        
class SolarLabel(tk.Label):
    ## @brief Initializes an SolarLabel object.
    # @param parent The parent tkinter widget for the solar label.
    # @param **kwargs Additional keyword arguments for the tkinter Label widget.
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        font_size = int(screen_height * (100/1440))
        
        self.label_solar = tk.Label(self, font = ('Verdana', font_size))
        self.label_solar.pack()
    
    ## @brief Sets the solar value to be displayed.
    # @param value The solar value.
    def setS(self, value):
        self.label_solar.config(text=value)
        
    ## @brief Shows the solar label.
    def show(self):
        self.place(relx=0.8, rely=0.5, anchor = 'center')  
    
    ## @brief Hides the solar label.
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
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        button_width = int(screen_width * 0.0075)
        comp_button_width = int(screen_width * 0.01)
        button_height = int(screen_height * 0.0025)
        button_font_size = int(screen_height * (36/1440))
        welcome_font_size = int(screen_height * (40/1440))
        
        # Image dimensions when screen is 1440x900
        target_width = 1151
        target_height = 540
        
        welcome = tk.Label(self, text='Welcome!', font=('Verdana', welcome_font_size, 'bold'))
        welcome.place(relx=0.5, rely=0.1, anchor='center')
        
        button = tk.Button(self, text='Competition Mode', command=lambda: controller.show_frame(CompMode), font=('Arial', button_font_size, 'bold'))
        button.configure(width = comp_button_width, height = button_height)
        button.place(relx=0.25, rely=0.9, anchor='center')

        button2 = tk.Button(self, text='Grid Mode', command=lambda: controller.show_frame(Grid), font=('Arial', button_font_size, 'bold'))
        button2.configure(width = button_width, height = button_height)
        button2.place(relx=0.75, rely=0.9, anchor='center')
        
        # Add the image
        image_path = 'ElectricalSystem.png'

        # Calculate the scale factor based on the screen size and target size
        scale_factor = min(screen_width / 1440, screen_height / 900)

        # Calculate the scaled size of the image
        image_width = int(target_width * scale_factor)
        image_height = int(target_height * scale_factor)

        # Open the image
        image = Image.open(image_path)

        # Resize the image to the calculated size
        image = image.resize((image_width, image_height), Image.LANCZOS)

        # Create a PhotoImage object from the resized image
        photo = ImageTk.PhotoImage(image)

        # Create a label and assign the image to it
        image_label = tk.Label(self, image=photo)
        image_label.image = photo  # Keep a reference to prevent image from being garbage collected

        # Place the label in the frame
        image_label.place(relx=0.5, rely=0.45, anchor='center')

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
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        welcome_font_size = int(screen_height * (80/1440))
        text_font_size = int(screen_height * (40/1440))
        
        welcome = tk.Label(self, text='Welcome to the Competition Mode!', font = ('Verdana', welcome_font_size))
        welcome.place(relx=0.5, rely=0.3, anchor='center')
        
        usernameLabel = tk.Label(self, text="User Name", font = ('Verdana', text_font_size, 'bold'))
        usernameLabel.place(relx=0.5, rely=0.4, anchor='center')
        
        global username
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=username, font = ('Verdana', text_font_size))
        usernameEntry.place(relx=0.5, rely=0.45, anchor='center')
        
        def onClick():
            tkinter.messagebox.showinfo('Demo', 'Username Saved!')
            
        button = tk.Button(self, text='Enter', command=onClick, font = ('Verdana', text_font_size), bg='lightblue', fg='black')
        button.place(relx=0.5, rely=0.5, anchor='center')
        
        button2 = tk.Button(self, text='Start Competition Mode', command=lambda: controller.show_frame(GraphPage),
                    font = ('Verdana', text_font_size))
        button2.place(relx=0.5, rely=0.6, anchor='center')
        
        difficulty_instructions = tk.Label(self, text = "Adjust 3 way dial to change difficulty", font = ('Verdana', text_font_size)).place(relx=0.5, rely=0.7, anchor='center')
        difficulty = tk.Label(self, text = "Left = Easy     Middle = Medium     Right = Hard", font = ('Verdana', text_font_size)).place(relx=0.5, rely=0.75, anchor='center')
           
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
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        button_width = int(screen_width * 0.0075)
        button_height = int(screen_height * 0.0025)
        frame_font_size = int(screen_height * (20 / 1440))
        button_font_size = int(screen_height * (36 / 1440))
        welcome_font_size = int(screen_height * (40 / 1440))
        timer_font_size = int(screen_height * (50 / 1440))
        speed_title_size = int(screen_height * (20 / 1440))
        
        self.count = 5
        self.time = 10
        
        # Size scaling for Speed Meter
        meter_scaling = min(screen_height / 900, screen_width / 1440)
        adjusted_radius = 260 * meter_scaling # 260 is the radius at 1440 and 900
        
        # Size scaling for label frames
        frame_height_scaling = screen_height / 900
        frame_width_scaling = screen_width / 1440
        adjusted_height = frame_height_scaling * 100
        adjusted_width = frame_width_scaling * 150
        
        # For the current graph
        current_canvas = graph(self, title='Current Graph', ylabel='Current (A)', xlabel='Time (s)', label='Current (A)', ylim = 15, color='c')
        current_canvas.configure(borderwidth = 10, relief = 'solid')
        current_canvas.place(x = 0.007 * screen_width, y = 0.056*screen_height)
        
        # For the voltage graph
        voltage_canvas = graph(self, title='Voltage Graph', ylabel='Voltage (V)', xlabel='Time (s)', label='Voltage (V)', ylim = 150, color='g')
        voltage_canvas.place(x = 0.007 * screen_width, y = 0.5 * screen_height)
        
        # For the power graph
        power_canvas = graph(self, title='Power Graph', ylabel='Power (W)', xlabel='Time (s)', label='Power (W)', ylim = 550, color='b')
        power_canvas.place(x = 0.417 * screen_width, y = 0.056 * screen_height)
        
        energy_frame = tk.LabelFrame(self, text='Cumulative Energy (J)', height = adjusted_height, width = adjusted_width, font = ('Verdana', frame_font_size)).place(relx=0.694, rely=0.667)
        
        energy = EnergyLabel(energy_frame)
        energy.place(relx=0.5, rely=0.5)
        
        timer_frame = tk.LabelFrame(self, text='Countdown (s)', height = adjusted_height, width = adjusted_width, font = ('Verdana', frame_font_size))
        timer_frame.place(relx=0.833, rely=0.111)
        
        timer_label = tk.Label(timer_frame, text='5', font=('Verdana', timer_font_size))
        timer_label.place(relx = 0.5, rely = 0.45, anchor = 'center')
        
        speed_meter_title = tk.Label(self, text = "Electrical Frequency (Hz)", font = ('Verdana', speed_title_size)).place(relx = 0.5, rely = 0.53, anchor = 'center')
        
        speed = Meter(self, radius=adjusted_radius, start=0, end=220, border_width=0,
               fg="black", text_color="white", start_angle=270, end_angle=-270,
               text_font="DS-Digital 30", major_divisions=20, minor_divisions = 5, scale_color="white", needle_color="red")
        
        speed.place(relx=0.417, rely = 0.556)
        
        # Function that uploads the competition mode code to the Arduino, opens the serial port and starts displaying the data
        def get_data():
            os.system('arduino-cli compile -b arduino:avr:mega /Users/tadiwadzvoti/Documents/Arduino/C_Mode_Working -u -p /dev/cu.usbmodem1301')
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
        
        
        button1 = tk.Button(self, text="Start", command = start).place(relx=0.9, rely=0.75)
        
        button2 = tk.Button(self, text="Leaderboard", command = deletetext).place(relx=0.9, rely=0.8)
        
        button3 = tk.Button(self, text = "Quit", command = quit).place(relx=0.9, rely=0.85)

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
        
        # Styling options
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        font_scaling = screen_height / 1440
        
        title_font = ("Arial", int(40 * font_scaling), "bold")
        listbox_font = ("Arial", int(30 * font_scaling))
        listbox_width = int((40/1440) * screen_width)
        listbox_height = int((20/900) * self.winfo_screenmmheight())
        
        # Flag to check state of leaderboard view
        self.flag_v = True
        
        # creation of daily leaderboard
        daily_leaderboard_data = []
        
        daily_leaderboard_title = tk.Label(self, text = "Daily Leaderboard", font = title_font)
        daily_leaderboard_title.place(relx=0.02, rely=0.05, anchor='w')
      
        daily_leaderboard = tk.Listbox(self, width = listbox_width, height = listbox_height, font = listbox_font)
        daily_leaderboard.place(relx = 0.02, rely = 0.18, anchor='w')    
        
        # creation of all time leaderboard
        all_leaderboard_data = []
        
        all_leaderboard_title = tk.Label(self, text = "All Time Leaderboard", font = title_font)
        all_leaderboard_title.place(relx=0.98, rely=0.05, anchor='e')
        
        all_leaderboard = tk.Listbox(self, width = listbox_width, height = listbox_height, font = listbox_font)
        all_leaderboard.place(relx = 0.98, rely = 0.18, anchor='e')   
           
        def update_board():
            daily_leaderboard.delete(0, tk.END)
            daily_leaderboard_data.clear()
            
            all_leaderboard.delete(0, tk.END)
            all_leaderboard_data.clear()
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                for i in reader:
                    if i != '' and i[0] != 'UserName':
                        all_leaderboard_data.append(i)
                        if i[3] == str(date.today()):
                            daily_leaderboard_data.append(i)
            all_leaderboard_data.sort(key = lambda max_p: float(max_p[1]), reverse = True)
            daily_leaderboard_data.sort(key = lambda max_p: float(max_p[1]), reverse = True)
        
            for rank, row in enumerate(daily_leaderboard_data, start=1):
                daily_leaderboard.insert(tk.END, f"{rank}. {row[0]} - Maximum Power (W): {row[1]}")
            daily_leaderboard.update()
            
            for rank1, row1 in enumerate(all_leaderboard_data, start=1):
                all_leaderboard.insert(tk.END, f"{rank1}. {row1[0]} - Maximum Power (W): {row1[1]}" )
            all_leaderboard.update()    
        
        def change_view(flag):
            all_leaderboard.delete(0, tk.END)
            daily_leaderboard.delete(0, tk.END)
            if flag == True:
                all_leaderboard_data.sort(key = lambda max_e: float(max_e[2]), reverse = True)
                daily_leaderboard_data.sort(key = lambda max_e: float(max_e[2]), reverse = True)
                
                for rank, row in enumerate(daily_leaderboard_data, start=1):
                    daily_leaderboard.insert(tk.END, f"{rank}. {row[0]} - Cumulative Energy (J): {row[2]}")
                    daily_leaderboard.update()
                
                for rank1, row1 in enumerate(all_leaderboard_data, start=1):
                    all_leaderboard.insert(tk.END, f"{rank1}. {row1[0]} - Cumulative Energy (J): {row1[2]}" )
                    all_leaderboard.update() 
                view_change.config(text = 'View Power') 
                
                
            else:
                all_leaderboard_data.sort(key = lambda max_p: float(max_p[1]), reverse = True)
                daily_leaderboard_data.sort(key = lambda max_p: float(max_p[1]), reverse = True)
                
                for rank, row in enumerate(daily_leaderboard_data, start=1):
                    daily_leaderboard.insert(tk.END, f"{rank}. {row[0]} - Maximum Power (W): {row[1]}")
                    daily_leaderboard.update()
                
                for rank1, row1 in enumerate(all_leaderboard_data, start=1):
                    all_leaderboard.insert(tk.END, f"{rank1}. {row1[0]} - Maximum Power (W): {row1[1]}" )
                    all_leaderboard.update() 
                view_change.config(text = 'View Energy')
            
            
        def up_lb():
            t_lb = threading.Thread(target=update_board)
            t_lb.start()
        
        def change():
            t_change = threading.Thread(target = change_view(self.flag_v))
            t_change.start()
            self.flag_v = ~self.flag_v
             
        update_leaderboard = tk.Button(self, text = 'Update', command = up_lb)
        update_leaderboard.place(relx = 0.5, rely = 0.08, anchor='center')
        
        view_change = tk.Button(self, text = 'View Energy', command = change)
        view_change.place(relx = 0.5, rely = 0.15, anchor = 'center')
        
        back_to_comp = tk.Button(self, text = 'Competition Mode', command = lambda : controller.show_frame(CompMode))
        back_to_comp.place(relx = 0.5, rely = 0.3, anchor='center')
        
        back_to_home = tk.Button(self, text = 'Home', command = lambda : controller.show_frame(Home))
        back_to_home.place(relx = 0.5, rely = 0.35, anchor = 'center')
        
        button3 = tk.Button(self, text = "Quit", command = quit)
        button3.place(relx = 0.5, rely = 0.4, anchor='center')
        
        #jelly = tk.Label(self, text = 'ADD FOOD EQUIVALENT', font = 'Verdana 30')
       # jelly.place(relx = 0.5, rely = 0.8, anchor='center')

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
        
        screen_height = self.winfo_screenheight()
        screen_width = self.winfo_screenwidth()
        font_scaling = screen_height / 1440
        speed_title_size = int(60 * font_scaling)
        
        # Size scaling for Speed Meter
        meter_scaling = min(screen_height / 900, screen_width / 1440)
        adjusted_radius = 360 * meter_scaling
        
        # Size scaling for label frames
        frame_height_scaling = screen_height / 900
        frame_width_scaling = screen_width / 1440
        border_thickness = 10 * min(screen_height / 900, screen_width / 1440)
        adjusted_height = frame_height_scaling * 200
        adjusted_width = frame_width_scaling * 300
        
        title_label = tk.Label(self, text = "Grid Mode", font = ("Verdana", int(80 * font_scaling), 'bold')).place(relx = 0.5, rely = 0.1, anchor = 'center')
        
        instructions = tk.Label(self, text = "Stay within the 35 - 65 Hz threshold to activate the loads", font = ("Verdana", int(50 * font_scaling))).place(relx = 0.5, rely = 0.2, anchor = 'center')
        
        instructions2 = tk.Label(self, text = "If you fall out of the threshold for 5 seconds grid mode ends", font = ("Verdana", int(50 * font_scaling))).place(relx = 0.5, rely = 0.25, anchor = 'center')
        
        wind_frame = tk.LabelFrame(self, text='Wind Turbine Voltage (V)', height = adjusted_height, width = adjusted_width, borderwidth = border_thickness).place(relx=0.1, rely=0.5, anchor = 'w')
        
        wind = WindLabel(wind_frame)
        
        solar_frame = tk.LabelFrame(self, text='Solar Panel Voltage (V)', height = adjusted_height, width = adjusted_width, borderwidth = border_thickness).place(relx=0.9, rely=0.5, anchor = 'e')
        
        solar = SolarLabel(solar_frame)
        
        speed_meter_title = tk.Label(self, text = "Electrical Frequency (Hz)", font = ('Verdana', speed_title_size)).place(relx = 0.5, rely = 0.75, anchor = 'center')
        
        speed = Meter(self, radius=adjusted_radius, start=0, end=90, border_width=0,
               fg="black", text_color="white", start_angle=270, end_angle=-270,
               text_font="DS-Digital 30", scale_color="white", needle_color="red")
        speed.set_mark(65, 90, 'red')
        speed.set_mark(35, 65, 'green')
        speed.set_mark(0, 35, 'yellow')
        speed.place(relx = 0.5, rely = 0.5, anchor = 'center')
        
        def get_data_grid():
            os.system('arduino-cli compile -b arduino:avr:mega /Users/tadiwadzvoti/Documents/4th_Year_Project/Code/Arduino/TestGrid -u -p /dev/cu.usbmodem1301')
            ser = serial.Serial('/dev/cu.usbmodem1301', 9600)
            while True:
                try:
                    pulldata = ser.readline()
                    string = pulldata.decode()
                    stripped_string = string.strip()
                    get_data = stripped_string.split(',')
                    if(get_data[0] != 'DONE'):
                        speed.set(float(get_data[0]))
                        wind.setW(float(get_data[1]))
                        solar.setS(float(get_data[2])) 
                    else:
                        pause
                        break
                except ValueError:
                    pause
                    break
                
        def start():  
            speed.set(0)
            wind.setW(0)
            wind.show()
            solar.setS(0)
            solar.show()
            
            t = threading.Thread(target=get_data_grid)   
            t.start()
        
        def back_to_home():
            pause()
            wind.hide()
            solar.hide()
            controller.show_frame(Home)
            
        button1 = tk.Button(self, text="Start", command = start).place(relx=0.9, rely=0.8)
        
        button2 = tk.Button(self, text = "Back to Home", command = back_to_home).place(relx = 0.9, rely = 0.85)
        
        button3 = tk.Button(self, text = "Quit", command = quit).place(relx=0.9, rely=0.9)
    
# Driver code
app = GUI()
app.mainloop()    
