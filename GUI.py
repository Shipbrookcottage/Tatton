# source of code https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/

import tkinter as tk 
import matplotlib
import urllib
import json
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import style
from matplotlib.figure import Figure
import matplotlib.animation as animation

LARGEFONT = ("Verdana", 35)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi = 100)
a = f.add_subplot(111)

def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    
    a.clear()
    a.plot(xList, yList) 
    
    

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
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        
        
     
# Driver code
app = displayApp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
             
         