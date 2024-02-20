#!/usr/bin/env python3
import tkinter as tk
#import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile
import sys
from sys import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import numpy as np
#import serial
#import io



#style setup
main_color = '#FFFFFF'
header_color = '#000000'
sidebar_color = "#FFFFFF"
outline_color = '#000000'
frame_color = '#c0c0c0'
fontHeader=('Inter',18, "bold")
fontGroups=("Inter", 14, "bold")
fontButtons=("Inter", 10, "bold")
xAxis="Time (s)"
yAxis="Force Gravity (g)"
p_x = 0.1
p_y = 0.2 

BAUD_RATE = 9600
BYTES_RECORDED = 1000
SERIAL_PORT="COM3"
#5 to 40 Hz band pass filter as Liz

#filepath = "/home/LucyDropTower/Documents/lucy-drop-gui-/"
masterName=[['DeepPink','Hotpink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Navy','Purple','Grey','Black'],[],[]]
t = []
s = []
m = []



groupData=[[[],[],[]],[[],[],[]]]

mu, sigma = 30, .1

for x in range(len(masterName[0])):
    masterName[1].append('Group: '+f'{x+1}')
    masterName[2].append('Group: '+f'{x+1} Settings')
    groupData[0][0].append([]) #Create TRIAL 1 GROUP X t
    groupData[0][1].append([]) #Create TRIAL 1 GROUP X s
    groupData[0][2].append([]) #Create TRIAL 1 GROUP X m
    groupData[1][0].append([]) #Create TRIAL 2 GROUP X t
    groupData[1][1].append([]) #Create TRIAL 2 GROUP X s
    groupData[1][2].append([]) #Create TRIAL 2 GROUP X m
    t.append([])
    s.append([])
    m.append([])



  
  
class App(tk.Tk):
    def __init__(self):  
        super().__init__()
    #Window Builder
        self.title('Lucy Drop Tower')
        window_width = 1920-200
        window_height = 1080-200
        self.geometry(f'{window_width}x{window_height}')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()    
        print(screen_height)
        print(screen_width)
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        #self.eval('tk::PlaceWindow . center')
        self.tk.call('tk', 'scaling', 1.25)

        if platform == "linux" or platform == "linux2":
            # linux
            #self.attributes('-type', 'splash')
            self.resizable(0,0)
        elif platform == "darwin":
            # OS X
            self.resizable(0,0)
            #self.attributes('-type', 'splash')
        elif platform == "win32":
            # Windows...
            icon = tk.PhotoImage(file = './assets/icon.png') 
            self.iconphoto(False, icon) 
            self.minsize(window_width,window_height)


    #Macros
        self.bind("<Escape>", lambda command: exit())
        self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        


    #Frame Builder
        self.sidebarFrame = tk.Frame(self)
        self.sidebarFrame.config(highlightbackground=outline_color,highlightthickness=1,pady=1,padx=5)
        self.sidebarFrame.place(relx=0, rely=0, relwidth=p_x, relheight=1)
        
        self.headerFrame = tk.Frame(self)
        self.headerFrame.config(background=header_color,highlightbackground=outline_color,highlightthickness=1,pady=15,padx = 15)
        self.headerFrame.place(relx=p_x, rely=0, relwidth=1-p_x, relheight=p_y)
        
        self.mainFrame = tk.Frame(self)
        self.mainFrame.configure(highlightbackground=outline_color,highlightthickness=1)
        self.mainFrame.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
  

        self.topFrame = tk.Frame(self.headerFrame)
        self.topFrame.config(highlightbackground=outline_color,highlightthickness=1)
        self.topFrame.pack(expand = True, fill ='both')
        self.topFrame.rowconfigure(0,weight = 1,)
        self.topFrame.columnconfigure(0,weight = 1,uniform='a')
        self.topFrame.columnconfigure(1,weight = 2,uniform='a')
        self.topFrame.columnconfigure(2,weight = 1,uniform='a')


    # Top Settings Frame
        self.topSettingsFrame = tk.Frame(self.topFrame)
        self.topSettingsFrame.config(highlightbackground=outline_color,highlightthickness=2)
        self.topSettingsFrame.grid(row = 0, column =0,sticky='news')
        self.topSettingsFrame.rowconfigure((0,1),weight = 1,uniform='a')
        self.topSettingsFrame.columnconfigure((0,1),weight = 1,uniform='a')
        global com
        BAUD_RATE = 9600
        com=tk.StringVar(self)
        com.set("COM1")
        comSLCT=tk.OptionMenu(self.topSettingsFrame,com,'COM1','COM2','COM3','COM4')
        comSLCT.grid(row = 0, column =0)
        comShowBTN=tk.Button(self.topSettingsFrame,text='COM CHECK FUNCTION',font=fontButtons,command=self.fComUpdate)
        comShowBTN.grid(row = 0, column =1)
        #Save/Load
        readBTN=tk.Button(self.topSettingsFrame,font=fontButtons,text="Load File", command=self.fLoad)
        readBTN.grid(row = 1, column =0)
        writeBTN=tk.Button(self.topSettingsFrame,font=fontButtons,text="Save File", command=self.fSave)
        writeBTN.grid(row = 1, column =1)



    # Top Run Frame
        self.topRunFrame = tk.Frame(self.topFrame)
        self.topRunFrame.config(highlightbackground=outline_color,highlightthickness=2)
        self.topRunFrame.grid(row = 0, column =1,sticky='news')
        self.topRunFrame.rowconfigure(0,weight = 1)
        self.topRunFrame.rowconfigure((0,1,2),weight = 1)
        self.topRunFrame.columnconfigure((0,1),weight = 1,uniform='a')
        global mainLab
        mainLab = tk.Label(self.topRunFrame,font=fontHeader)
        mainLab.grid(row = 0, column =0)
        rnBTN=tk.Button(self.topRunFrame,font=fontHeader,text="Run Dropper Function",command=self.fDropper)
        rnBTN.grid(row = 0, column =1)
        
        self.trialSelection = tk.IntVar()
        tk.Radiobutton(self.topRunFrame,variable=self.trialSelection, value=0,command=self.fShow, text=' Trial 1 ', font=fontGroups, indicatoron=0,bg='white',fg='black').grid(row = 2, column=0)
        tk.Radiobutton(self.topRunFrame,variable=self.trialSelection, value=1,command=self.fShow, text=' Trial 2 ',font=fontGroups, indicatoron=0,bg='white',fg='black').grid(row = 2, column=1)

    # Top Finally Frame
        self.sidebarFinallyFrame = tk.Frame(self.topFrame)
        self.sidebarFinallyFrame.config(pady=5,padx=5,highlightbackground=outline_color,highlightthickness=2)
        self.sidebarFinallyFrame.grid(row = 0, column =2,sticky='news') 

        finallyBTN=tk.Button(self.sidebarFinallyFrame,font=fontButtons,text="Finally",background='white',command=self.fFinally)
        finallyBTN.pack(expand = False, fill ='both')




    # SideBar Setup
        self.userSelection = tk.IntVar()
        for i in range(len(masterName[0])):
            self.groupFrame=tk.Frame(self.sidebarFrame)
            self.groupFrame.config(background = masterName[0][i],pady=5,padx=5,highlightbackground=outline_color,highlightthickness=2)
            self.groupFrame.pack(expand = True , fill ='both')
            self.groupFrame.rowconfigure(0,weight = 1)
            self.groupFrame.columnconfigure((0),weight = 1)
            
            tk.Radiobutton(self.groupFrame,variable=self.userSelection, value=i,command=self.fShow, indicatoron=0,bg='white',font=fontGroups,text = masterName[1][i],fg='black',highlightbackground=outline_color,highlightthickness=1.5).grid(row = 0, column=0)


      

    #PLOT
        self.plotFrame = tk.Frame(self.mainFrame)
        self.plotFrame.pack()
        self.plotFrame.configure(highlightbackground=outline_color,highlightthickness=10)
        fig = plt.Figure(facecolor="#c0c0c0") 
        global ax
        ax = fig.add_subplot(111) 
        global graph
        graph = FigureCanvasTkAgg(fig, master=self.plotFrame) 
        graph.get_tk_widget().pack(fill='both',expand=True) 
        self.fShow()
        

    def fFinally(self):
        print("Finally function")
        finallyPopUp()

    def fLoad(self):
        print("Load function")
        filename=askopenfile()
        print(filename)

    def fSave(self):
        print("Save function")
        filename=asksaveasfile()
        
    def fComUpdate(self):
        SERIAL_PORT = str(com.get())
        print("Value Selected is: "+com.get())
        print("Value of Serial Port STR is: "+SERIAL_PORT)

    def fShow(self):
        i = self.userSelection.get()
        mainLab["text"]=masterName[2][i]
        self.plotFrame.configure(highlightcolor=masterName[0][i])
        self.headerFrame.configure(bg=masterName[0][i])
        ax.cla()
        ax.set_xlabel(xAxis) 
        ax.set_ylabel(yAxis) 
        ax.grid()
        ax.plot(t[i],s[i],color=masterName[0][i])
        graph.draw()  
    
    def fDropper(self):
        i = self.userSelection.get()
        t[i]=(np.arange(0, 20, .5))
        s[i]=(np.random.normal(mu, sigma, len(t[i])))
        m[i]=max(s[i])
        #print("MAX VALUE LIST M: "+f'{m}')
        ax.cla()
        ax.set_xlabel(xAxis) 
        ax.set_ylabel(yAxis) 
        ax.grid()
        ax.plot(t[i],s[i],color=masterName[0][i])
        graph.draw() 

    def fQuit(self):
        exit()


class finallyPopUp(tk.Tk):
    def __init__(self):
        super().__init__()
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
        self.title('Lucy Drop Tower')  
        


        self.mainloop()

      

if __name__ == "__main__":
    app=App()
    app.mainloop()
    
    
