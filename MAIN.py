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
p_x = 0.15 
p_y = 0.05  


#filepath = "/home/LucyDropTower/Documents/lucy-drop-gui-/"
masterName=[['DeepPink','Hotpink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Navy','Purple','Grey','Gray10'],[],[]]
t = []
s = []

mu, sigma = 30, 0.6 


for x in range(len(masterName[0])):
    masterName[1].append('Group: '+f'{x+1}')
    masterName[2].append('Showing Group: '+f'{x+1}')
    t.append([])
    s.append([])

  
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
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.attributes('-type', 'splash')
        #icon = tk.PhotoImage(file = './assets/icon.png') 
        #self.iconphoto(False, icon) 
        #self.resizable(0,0)
        self.title('Lucy Drop Tower')
          
    
    #Macros
        #self.bind("<Escape>", lambda command: exit())
        #self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        


    #Frame Builder
        self.sidebarFrame = tk.Frame(self)
        self.sidebarFrame.config(highlightbackground=outline_color,highlightthickness=1,pady=5,padx=5)
        self.sidebarFrame.place(relx=0, rely=p_y, relwidth=p_x, relheight=1)
        
        self.headerFrame = tk.Frame(self)
        self.headerFrame.config(background=header_color,highlightbackground=outline_color,highlightthickness=1,padx = 20)
        self.headerFrame.place(relx=0, rely=0, relwidth=1, relheight=p_y)
        
        self.mainFrame = tk.Frame(self)
        self.mainFrame.configure(bg=main_color,highlightbackground=outline_color,highlightthickness=1,pady=5)
        self.mainFrame.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        
        self.selection = tk.IntVar()
    #Header Setup
        xBTN=tk.Button(self.headerFrame,command= self.fQuit,text="Close (X)",font=fontButtons)
        xBTN.pack(side=tk.RIGHT)

    #Main Window Setup
        global mainLab
        mainLab = tk.Label(self.mainFrame,bg=main_color,font=fontHeader,text='')
        mainLab.pack()

        rnBTN=tk.Button(self.mainFrame,font=fontHeader,text="Run Dropper Function",command=self.fDropper)
        rnBTN.pack()
    
       

    #SideBar Setup
        for i in range(len(masterName[0])):
            self.groupFrame=tk.Frame(self.sidebarFrame)
            color = masterName[0][i]
            self.groupFrame.config(background = color,pady=10,padx=5)

            #grid layout
            self.groupFrame.rowconfigure(0,weight = 0)
            self.groupFrame.columnconfigure((0,1),weight = 1,uniform='a')
            
            tk.Label(self.groupFrame,bg='white',font=fontGroups,text = masterName[1][i],highlightbackground=outline_color,highlightthickness=1.5).grid(row = 0, column =0)
            tk.Radiobutton(self.groupFrame,variable=self.selection, value=i,command=self.fShow, indicatoron=1,bg=color,fg='black').grid(row = 0, column=1)
            
            self.groupFrame.pack(expand = False, fill ='both')
    
        

    #PLOT
        self.plotFrame = tk.Frame(self.mainFrame)
        fig = plt.figure(figsize=(16, 8))
        plt.ion()
        
        canvas = FigureCanvasTkAgg(fig, self.plotFrame)
        toolbar = NavigationToolbar2Tk(canvas, self.plotFrame)
        toolbar.update()
        canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        self.plotFrame.pack(fill=tk.BOTH, expand=1)
        
        
        self.fShow()
    

    def fQuit(self):
        exit()



    def fShow(self):
        index = self.selection.get()
        mainLab["text"]=masterName[2][index]
        self.headerFrame.configure(bg=masterName[0][index])
        plt.cla()
        plt.plot(t[index],s[index],color=masterName[0][index])
        plt.draw()  
    
    def fDropper(self):
        index = self.selection.get()
        self.fUpdate()
        plt.cla()
        plt.plot(t[index],s[index],color=masterName[0][index])
        plt.draw()  

    def fUpdate(self):
        index = self.selection.get()
        t[index]=(np.arange(0, 5, .02))
        s[index]=(np.random.normal(mu, sigma, len(t[index])))
    
"""
class popUP(tk.Tk):
    def __init__(self,index):
        super().__init__()
        color = masterName[0][index]
        labelText = masterName[1][index]
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
        self.mainFrameloop()
"""
      

if __name__ == "__main__":
    app=App()
    app.mainloop()
    
