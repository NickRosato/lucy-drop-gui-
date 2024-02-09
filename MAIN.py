#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
import sys
from sys import platform
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
master=[['DeepPink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Magenta','Purple','Navy','Grey','Black'],[],[]]
t = []
s = []

for index in range(len(master[0])):
    master[1].append('Group: '+f'{index+1}')
    master[2].append('Showing Group: '+f'{index+1}')


#s = np.sin(np.pi*t)


#data={}
#data[0]=np.arange(0, 3, .01)
#data[1]= 2 * np.sin(2 * np.pi * data[0])



#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file

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

        tk.Button(self.header,text="Update",command=self.changeNUM).pack()
    
       

    #SideBar Setup
        for i in range(len(master[0])):
            #groupSeg(self.sidebar,index).pack(expand = False, fill ='both')
            self.group=tk.Frame(self.sidebar)
            color = master[0][i]
            self.group.config(background = color,pady=10,padx=5)

            #grid layout
            self.group.rowconfigure(0,weight = 0)
            self.group.columnconfigure((0,1,2),weight = 1,uniform='a')
            
            tk.Label(self.group,bg='white',font=fontGroups,text = master[1][i],highlightbackground=outline_color,highlightthickness=1.5).grid(row = 0, column =0)
            tk.Radiobutton(self.group,variable=self.selection, value=i,command=self.show_selection, indicatoron=1,bg=color,fg='black').grid(row = 0, column=1)
            #tk.Button(self.group,text = "Display",font=fontButtons,bg='white',fg='black').grid(row = 0, column=2)
            
            self.group.pack(expand = False, fill ='both')
    
        self.show_selection()
    #PLOT
        f0 = tk.Frame(self.main)
        f0.pack()
        fig = plt.figure(figsize=(16, 12))
        plt.ion()
        
        canvas = FigureCanvasTkAgg(fig, f0)
        plot_widget = canvas.get_tk_widget()
        
        plot_widget.pack(fill=tk.BOTH, expand=1)
        plt.cla()

    #mainloop init
        self.mainloop()

        
    def changeNUM(self):
        #plt.cla()
        t = np.arange(0.0,3.0,0.01)
        s = np.sin(np.pi*t)
        plt.plot(t,s)
        plt.draw()  

    def update(self):
        index = self.selection.get()
        plt.cla()
        plt.plot(t,s)
        plt.draw()  

    def show_selection(self):
        self.update()
        index = self.selection.get()
        mainLab["text"]=master[2][index]
        self.header.configure(bg=master[0][index])


if __name__ == "__main__":
    App()
