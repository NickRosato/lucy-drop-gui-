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
master=[['DeepPink','Hotpink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Navy','Purple','Grey','Gray10'],[],[]]
t = []
s = []

mu, sigma = 30, 0.6 


for x in range(len(master[0])):
    master[1].append('Group: '+f'{x+1}')
    master[2].append('Showing Group: '+f'{x+1}')
    t.append([])
    s.append([])

  

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file

class App(tk.Tk):
    def __init__(self):  
        super().__init__()
    #Window Builder
        window_width = 1920-100
        window_height = 1080-180
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.wm_geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.wm_minsize(window_width, window_height)
        #self.wm_attributes('-type', 'splash')
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
        self.main.configure(bg=main_color,highlightbackground=outline_color,highlightthickness=1,pady=5)
        self.main.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        
        self.selection = tk.IntVar()

    #Main Window Setup
        global mainLab
        mainLab = tk.Label(self.main,bg=main_color,font=fontHeader,text='Group: '+f'{1}')
        mainLab.pack()

        rnBTN=tk.Button(self.main,font=fontHeader,text="RUN DROPPER FUNCTION",command=self.dropper)
        rnBTN.pack()
    
       

    #SideBar Setup
        for i in range(len(master[0])):
            #groupSeg(self.sidebar,index).pack(expand = False, fill ='both')
            self.group=tk.Frame(self.sidebar)
            color = master[0][i]
            self.group.config(background = color,pady=10,padx=5)

            #grid layout
            self.group.rowconfigure(0,weight = 0)
            self.group.columnconfigure((0,1),weight = 1,uniform='a')
            
            tk.Label(self.group,bg='white',font=fontGroups,text = master[1][i],highlightbackground=outline_color,highlightthickness=1.5).grid(row = 0, column =0)
            tk.Radiobutton(self.group,variable=self.selection, value=i,command=self.show_selection, indicatoron=1,bg=color,fg='black').grid(row = 0, column=1)
            #tk.Button(self.group,text = "RUN",font=fontButtons,bg='white',fg='black').grid(row = 0, column=2)
            
            self.group.pack(expand = False, fill ='both')
    
        self.show_selection()
    #PLOT
        f0 = tk.Frame(self.main)
        f0.pack()
        fig = plt.figure(figsize=(16, 8))
        plt.ion()
        
        canvas = FigureCanvasTkAgg(fig, f0)
        plot_widget = canvas.get_tk_widget()
        
        plot_widget.pack(fill=tk.BOTH, expand=1)
        plt.cla()
        plt.plot(t[0],s[0],color=master[0][0])
        plt.draw() 

    
    #mainloop init
        self.mainloop()


    def dropper(self):
        index = self.selection.get()
        self.update()

        plt.cla()
        plt.plot(t[index],s[index],color=master[0][index])
        plt.draw()  

    def show_selection(self):
        index = self.selection.get()
        mainLab["text"]=master[2][index]
        self.header.configure(bg=master[0][index])
        plt.cla()
        plt.plot(t[index],s[index],color=master[0][index])
        plt.draw()  
    
    def update(self):
        index = self.selection.get()
        t[index]=(np.arange(0, 5, .02))
        s[index]=(np.random.normal(mu, sigma, len(t[index])))
    
class popUP(tk.Tk):
    def __init__(self,index):
        super().__init__()
        color = master[0][index]
        labelText = master[1][index]
        window_width = 480
        window_height = 480
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.wm_minsize(window_width, window_height)
        self.wm_resizable(0,0)
        self.wm_maxsize(window_width, window_height)
        self.wm_attributes('-topmost', 1)
        tk.Label(self,bg=color,text=index).pack()
        
        self.configure(bg=color)
        self.title('Lucy Drop Tower')
        self.mainloop()
        

if __name__ == "__main__":
    App()
    
