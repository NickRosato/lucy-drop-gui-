#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
import sys
from sys import platform
import matplotlib.pyplot as plt
import numpy as np
#import serial
#import io

#style setup
main_color = 'white'
header_color = '#E61231'
visualisation_frame_color = "#ffffff"
sidebar_color = "white"
outline_color = '#808080'
frame_color = 'grey'
fontHeader=("Arial", 15, "bold")
fontGroups=("Arial", 12, "bold")
fontButtons=("Arial", 10, "bold")
p_x = 0.15 # for 1920 : x = 288
p_y = 0.025  # for 1080 : y = 27


#filepath = "/home/LucyDropTower/Documents/lucy-drop-gui-/"

groupColor=['DeepPink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Magenta','Purple','Navy','Grey','Black']

"""
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller 
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS or _MEIPASS2
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
"""

class App(tk.Tk):
    def __init__(self):
        
        #main setup
        super().__init__()

        window_width = 1920
        window_height = 1080
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.minsize(window_width, window_height)
        
        icon = tk.PhotoImage(file = './assets/icon.png') 
        self.iconphoto(False, icon) 
        self.resizable(0,0)
        self.title('Lucy Drop Tower')
        self.bind("<Escape>", lambda event: exit())
        #self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.maxsize(window_width, window_height)
        
        """
        if platform == "linux" or platform == "linux2":
            # linux
            self.attributes("-zoomed", True)
        elif platform == "darwin":
            # OS X
            self.state("zoomed")
        elif platform == "win32":
            # Windows...
            self.state("zoomed")
        """

        #widgets
        self.sidebar = Sidebar(self)
        self.header = Header(self)
        self.main = Main(self)

        self.mainloop()



class Main(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg=main_color,highlightbackground=outline_color,highlightthickness=1)
        self.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)


class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(background=header_color,highlightbackground=outline_color,highlightthickness=1,padx = 20)
        self.place(relx=0, rely=0, relwidth=1, relheight=p_y)
           


class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(highlightbackground=outline_color,highlightthickness=1,pady=5,padx=5)
        self.place(relx=0, rely=p_y, relwidth=p_x, relheight=1)
    
        
        #lowerSize=4
        #rowSize=np.arange(0, len(groupColor)+lowerSize)
        #self.rowconfigure((0:len(groupColor)),weight = 1)
        #self.columnconfigure(0,weight = 0)
        for x in range(len(groupColor)):
            groupSeg(self,'Group: '+f'{x+1}',groupColor[x],x).pack(expand = False, fill ='both')


class groupSeg(tk.Frame):
    def __init__(self, parent,labelText,color,index):
        super().__init__(parent)
        self.config(background = color,pady=10,padx=5)

        #grid layout
        self.rowconfigure(0,weight = 0)
        self.columnconfigure((0,1,2),weight = 1,uniform='a')
        
        tk.Label(self,bg='white',font=fontGroups,text = labelText,highlightbackground=outline_color,highlightthickness=1.5).grid(row = 0, column =0)
        tk.Button(self,text = "Run",font=fontButtons,command= lambda:ButtonRUN(color,index),bg='white',fg='black').grid(row = 0, column=1)
        tk.Checkbutton(self,bg = color,fg='black').grid(row = 0, column = 2)
    

class ButtonRUN(tk.Tk):
    def __init__(self,color,index):
        super().__init__()

        window_width = 480
        window_height = 480
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.minsize(window_width, window_height)
        self.resizable(0,0)
        self.maxsize(window_width, window_height)
        self.attributes('-topmost', True)
        #icon = tk.PhotoImage(file = './assets/icon.png') 
        #self.iconphoto(False, icon) 
        
        self.configure(bg=color)
        self.title('Lucy Drop Tower')


        groupNumber=index+1

        text=("Button " + str(groupNumber) + " Pressed" )
        tk.Label(self,text=text,font=fontHeader).pack()
        self.mainloop()

App()