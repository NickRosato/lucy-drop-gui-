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
btnColor = '#cccccc'
btnColor_pressed = 'pink'
topBG='white'
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
masterName=[[],[],[]]
masterName[0]=['DeepPink','Hotpink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Navy','Purple','Grey','Black']

runTime=[[],[]]
runForce=[[],[]]
maxForce=[[],[]]

mu, sigma = 30, 5

for x in range(len(masterName[0])):
    masterName[1].append('Group: '+f'{x+1}') # Radio Button Name
    masterName[2].append('Group: '+f'{x+1} Settings') # Top Frame Header
    runTime[0].append([])
    runTime[1].append([])
    runForce[0].append([])
    runForce[1].append([])
    maxForce[0].append([])
    maxForce[1].append([])
  
  
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
        self.headerFrame.config(background=header_color,highlightbackground=outline_color,highlightthickness=1,pady=10,padx = 10)
        self.headerFrame.place(relx=p_x, rely=0, relwidth=1-p_x, relheight=p_y)
        

        self.topFrame = tk.Frame(self.headerFrame)
        self.topFrame.config(highlightbackground=outline_color,highlightthickness=1)
        self.topFrame.pack(expand = True, fill ='both')
        self.topFrame.rowconfigure(0,weight = 1,)
        self.topFrame.columnconfigure(0,weight = 1,uniform='a')
        self.topFrame.columnconfigure(1,weight = 2,uniform='a')
        self.topFrame.columnconfigure(2,weight = 1,uniform='a')


    # Top Settings Frame
        self.topSettingsFrame = tk.Frame(self.topFrame)
        self.topSettingsFrame.config(background=topBG,pady=5,padx=5,highlightbackground=outline_color,highlightthickness=2)
        self.topSettingsFrame.grid(row = 0, column =0,sticky='news')
        self.topSettingsFrame.rowconfigure((0,1),weight = 1,uniform='a')
        self.topSettingsFrame.columnconfigure((0,1),weight = 1,uniform='a')
        global com
        BAUD_RATE = 9600
        com=tk.StringVar(self)
        com.set("COM1")
        comSLCT=tk.OptionMenu(self.topSettingsFrame,com,'COM1','COM2','COM3','COM4')
        comSLCT.grid(row = 0, column =0)
        comShowbtnColor=tk.Button(self.topSettingsFrame,text='COM CHECK FUNCTION',font=fontButtons,command=self.fComUpdate)
        comShowbtnColor.grid(row = 0, column =1)
        #Save/Load
        readbtnColor=tk.Button(self.topSettingsFrame,font=fontButtons,text="Load File", command=self.fLoad)
        readbtnColor.grid(row = 1, column =0)
        writebtnColor=tk.Button(self.topSettingsFrame,font=fontButtons,text="Save File", command=self.fSave)
        writebtnColor.grid(row = 1, column =1)



    # Top Run Frame
        self.topRunFrame = tk.Frame(self.topFrame)
        self.topRunFrame.config(background=topBG,pady=5,padx=5,highlightbackground=outline_color,highlightthickness=2)
        self.topRunFrame.grid(row = 0, column =1,sticky='news')
        self.topRunFrame.rowconfigure(0,weight = 1)
        self.topRunFrame.rowconfigure((0,1,2),weight = 1)
        self.topRunFrame.columnconfigure((0,1),weight = 1,uniform="foo")
        global mainLab
        mainLab = tk.Label(self.topRunFrame,background=topBG,font=fontHeader)
        mainLab.grid(row = 0, column =0,sticky='ew',columnspan=2)
        rnbtnColor=tk.Button(self.topRunFrame,font=fontHeader,text="Run Dropper Function",background=btnColor,command=self.fDropper)
        rnbtnColor.grid(row = 1, column =0,sticky='ew',columnspan=2)
        
        self.trialSelection = tk.IntVar()
        tk.Radiobutton(self.topRunFrame,variable=self.trialSelection, value=0,command=self.fShow,indicatoron=0, selectcolor= btnColor_pressed,
                        text=' Trial 1 ', font=fontGroups, bg=btnColor,fg='black').grid(row = 2, column=0)
        tk.Radiobutton(self.topRunFrame,variable=self.trialSelection, value=1,command=self.fShow, indicatoron=0,selectcolor= btnColor_pressed,
                        text=' Trial 2 ',font=fontGroups, bg=btnColor,fg='black').grid(row = 2, column=1)

    # Top Finally Frame
        self.topMenuFrame = tk.Frame(self.topFrame)
        self.topMenuFrame.config(background=topBG,pady=5,padx=5,highlightbackground=outline_color,highlightthickness=2)
        self.topMenuFrame.grid(row = 0, column =2,sticky='news') 
        self.topMenuFrame.rowconfigure((0,1,2),weight = 1, uniform = 'a')
        self.topMenuFrame.columnconfigure(0,weight = 1)

        self.menuSelection = tk.IntVar()
        tk.Radiobutton(self.topMenuFrame,variable=self.menuSelection, value=0,command=self.fMenu1,indicatoron=0, selectcolor= btnColor_pressed,
                        text=' Show Single Graph ', font=fontGroups, bg=btnColor,fg='black').grid(row = 0, column=0,stick='ew')
        tk.Radiobutton(self.topMenuFrame,variable=self.menuSelection, value=1,command=self.fMenu2,indicatoron=0, selectcolor= btnColor_pressed,
                        text=' Show All Graphs ',font=fontGroups,bg=btnColor,fg='black').grid(row = 1, column=0,stick='ew')
        tk.Radiobutton(self.topMenuFrame,variable=self.menuSelection, value=2,command=self.fMenu3,indicatoron=0, selectcolor= btnColor_pressed,
                        text=' Show Ranking ',font=fontGroups,bg=btnColor,fg='black').grid(row = 2, column=0,stick='ew')


    # SideBar Setup
        self.userSelection = tk.IntVar()
        for i in range(len(masterName[0])):
            self.groupFrame=tk.Frame(self.sidebarFrame)
            self.groupFrame.config(background = masterName[0][i],pady=5,padx=5,highlightbackground=outline_color,highlightthickness=2)
            self.groupFrame.pack(expand = True , fill ='both')
            self.groupFrame.rowconfigure(0,weight = 1)
            self.groupFrame.columnconfigure((0),weight = 1)
            
            tk.Radiobutton(self.groupFrame,variable=self.userSelection, value=i,command=self.fShow, indicatoron=0, selectcolor= btnColor_pressed,
                            bg=btnColor,font=fontGroups,text = masterName[1][i],fg='black',highlightbackground=outline_color,highlightthickness=2,padx=5,pady=5).grid(row = 0, column=0)

      

    # Main Menu Frames
        self.mainFrame = tk.Frame(self)
        self.mainFrame.config(background='black',highlightbackground=outline_color,highlightthickness=1,pady=5,padx = 5)
        self.mainFrame.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)


        self.plotFrame = tk.Frame(self.mainFrame)
        self.plotFrame.config(highlightbackground=outline_color,highlightthickness=1)
        self.plotFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        fig = plt.Figure() 
        global ax
        ax = fig.add_subplot(111) 
        global graph
        graph = FigureCanvasTkAgg(fig, master=self.plotFrame) 
        graph.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        
        

        self.allFrame = tk.Frame(self.mainFrame)
        self.allFrame.config(background='red',highlightbackground=outline_color,highlightthickness=1)
        self.allFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        allFig = plt.Figure() 
        global allAX
        allAX = allFig.add_subplot(111) 
        global allGraph
        allGraph = FigureCanvasTkAgg(allFig, master=self.allFrame) 
        allGraph.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        self.rankFrame = tk.Frame(self.mainFrame)
        self.rankFrame.config(background='green',highlightbackground=outline_color,highlightthickness=1)
        self.rankFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        
        
        
        
        self.fShow()
        self.fMenu1()

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
        trl=self.trialSelection.get()
        i = self.userSelection.get()
        mainLab["text"]=masterName[2][i]
        self.headerFrame.configure(bg=masterName[0][i])

        ax.cla()
        ax.set_xlabel(xAxis) 
        ax.set_ylabel(yAxis) 
        ax.grid()
        if trl ==0:
            ax.plot(runTime[trl][i],runForce[trl][i],color=masterName[0][i])
        if trl ==1: 
            ax.plot(runTime[trl][i],runForce[trl][i],color=masterName[0][i],linestyle='dashed')
        graph.draw() 
    


    def fMenu1(self):
        self.plotFrame.tkraise()
    def fMenu2(self):
        self.allFrame.tkraise()
        allAX.cla()
        allAX.set_xlabel(xAxis) 
        allAX.set_ylabel(yAxis) 
        allAX.grid()
        for i in range(len(masterName[0])):
            allAX.plot(runTime[0][i],runForce[0][i],color=masterName[0][i])
            allAX.plot(runTime[1][i],runForce[1][i],color=masterName[0][i],linestyle='dashed')
        allGraph.draw()  

    def fMenu3(self):
        self.rankFrame.tkraise()
        
    def fDropper(self):
        trl=self.trialSelection.get()
        i = self.userSelection.get()
        runTime[trl][i]=(np.arange(0, 20, 5))
        runForce[trl][i]=(np.random.normal(mu, sigma, len(runTime[trl][i])))
        maxForce[trl][i]=max(runForce[trl][i])
        self.fShow()



    def fQuit(self):
        exit()

     

if __name__ == "__main__":
    app=App()
    app.mainloop()
    
    
