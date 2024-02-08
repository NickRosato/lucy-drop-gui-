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
sidebar_color = "white"
outline_color = '#808080'
frame_color = 'grey'
fontHeader=("Arial", 18, "bold")
fontGroups=("Arial", 12, "bold")
fontButtons=("Arial", 10, "bold")
p_x = 0.15 # for 1920 : x = 288
p_y = 0.025  # for 1080 : y = 27


#filepath = "/home/LucyDropTower/Documents/lucy-drop-gui-/"

groupColor=['DeepPink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Magenta','Purple','Navy','Grey','Black']
groups=[]
btnName=[]
for index in range(len(groupColor)):
    groups.append('Group: '+f'{index+1}')
    btnName.append('Display Group: '+f'{index+1}')
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
        super().__init__()
    #Window Builder
        window_width = 1920
        window_height = 1080
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.wm_geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.wm_minsize(window_width, window_height)
        icon = tk.PhotoImage(file = './assets/icon.png') 
        self.iconphoto(False, icon) 
        self.wm_resizable(0,0)
        self.title('Lucy Drop Tower')
        self.wm_maxsize(window_width, window_height)
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
    
    
    #Macros
        self.bind("<Escape>", lambda event: exit())
        #self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        


    #Frame Builder
        self.sidebar = tk.Frame(self)
        self.sidebar.config(highlightbackground=outline_color,highlightthickness=1,pady=5,padx=5)
        self.sidebar.place(relx=0, rely=p_y, relwidth=p_x, relheight=1)
        
        self.header = tk.Frame(self)
        self.header.config(background=header_color,highlightbackground=outline_color,highlightthickness=1,padx = 20)
        self.header.place(relx=0, rely=0, relwidth=1, relheight=p_y)
        
        self.main = tk.Frame(self)
        self.main.configure(bg=main_color,highlightbackground=outline_color,highlightthickness=1)
        self.main.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        
        self.selection = tk.IntVar()

    #Main Window Setup
        global mainLab
        mainLab = tk.Label(self.main,bg=main_color,font=fontHeader,text='Group: '+f'{1}')
        mainLab.pack()




    #SideBar Setup
        for i in range(len(groupColor)):
            #groupSeg(self.sidebar,index).pack(expand = False, fill ='both')
            self.group=tk.Frame(self.sidebar)
            color = groupColor[i]
            labelText = groups[i]
            self.group.config(background = color,pady=10,padx=5)

            #grid layout
            self.group.rowconfigure(0,weight = 0)
            self.group.columnconfigure((0,1,2),weight = 1,uniform='a')
            
            tk.Label(self.group,bg='white',font=fontGroups,text = labelText,highlightbackground=outline_color,highlightthickness=1.5).grid(row = 0, column =0)
            tk.Radiobutton(self.group,variable=self.selection, value=i,command=self.show_selection, indicatoron=1,bg=color,fg='black').grid(row = 0, column=1)
            #tk.Button(self.group,text = "Display",font=fontButtons,bg='white',fg='black').grid(row = 0, column=2)

            self.group.pack(expand = False, fill ='both')
    
        self.show_selection()

    
    #mainloop init
        self.mainloop()
            
    
    
    
    def show_selection(self):
        selected_option = self.selection.get()
        #print("selected", selected_option+1)
        lab= 'Group: '+f'{selected_option+1}'
        mainLab["text"]=lab







    






if __name__ == "__main__":
    App()
