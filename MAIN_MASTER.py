#!/usr/bin/env python3
__author__ = "Nicholas Rosato"
__copyright__ = "Copyright 2024, Collins Aerospace"
__credits__ = ["Nicholas Rosato","Stephen Kridel"]
__maintainer__ = "Nicholas Rosato"
__email__ = "nicholas.rosato@collins.com"


import tkinter as tk
#import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile
import sys
from sys import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd
import math
from serial.tools import list_ports
import serial
import time
import csv
from datetime import datetime


dropTime=2000
BAUD_RATE = 115200
SERIAL_PORT="COM3"

#ports = list_ports.comports()
#for port in ports: print(port)
#SERIAL_PORT = port[0]

#style setup
main_color = '#FFFFFF'
header_color = '#000000'
sidebar_color = "#FFFFFF"
figure_color= "#F0F0F0"
outline_color = '#000000'
frame_color = '#c0c0c0'
btnColor = '#cccccc'
btnColor_pressed = 'pink'
topBG='white'
fontHeader=('Inter',18, "bold")
fontGroups=("Inter", 14, "bold")
fontButtons=("Inter", 10, "bold")
xAxis="Time (s)"
yAxis="Gravitational Magnitude (g)"
p_x = 0.09
p_y = 0.175 

mu, sigma = 10, 1


trialNumber=2
cG1=['#FF0000','Red']
cG2=['#EE7600','Orange']
cG3=['#EEC900','Yellow']
cG4=['#006400','Green']
cG5=['#000080','Blue']
cG6=['#68228B', 'Purple']
cG7=['#FF1493','Pink']
cG8=['#630031','Maroon']
cG9=['#AB82FF','Lavender']
cG10=['#00CDCD','Turquoise']
cG11=['#7CFC00','Lime']
cG12=['#8B4513', 'Brown']
cG13=['#000000', 'Black']
cG14=['#616161', 'Grey']
colorHex=[cG1[0],cG2[0],cG3[0],cG4[0],cG5[0],cG6[0],cG7[0],cG8[0],cG9[0],cG10[0],cG11[0],cG12[0],cG13[0],cG14[0]]
colorName=[cG1[1],cG2[1],cG3[1],cG4[1],cG5[1],cG6[1],cG7[1],cG8[1],cG9[1],cG10[1],cG11[1],cG12[1],cG13[1],cG14[1]]

runLength=len(colorHex)*trialNumber

master=np.zeros(shape=(dropTime-1,runLength))


headerName=[[],[]]
runTime=[[],[]]
runForce=[[],[]]
maxForce=[[],[]]
groupName = [[],[]]

for x in range(len(colorHex)):
    groupName[0].append('Group: '+f'{x+1} Trial 1')
    groupName[1].append('Group: '+f'{x+1} Trial 2')
    headerName[0].append('Group: '+f'{x+1}') # Radio Button Name
    headerName[1].append('('+f'{colorName[x]}' ') Group: '+f'{x+1} Settings') # Top Frame Header
    runTime[0].append([])
    runTime[1].append([])
    runForce[0].append([])
    runForce[1].append([])
    maxForce[0].append(0)
    maxForce[1].append(0)


groupNameLegend=groupName[0]+groupName[1]

now = datetime.now()
fileNameMaster = "LUCY-DATE-"+now.strftime("%d-%m-%Y")+"-TIME-"+now.strftime("%H-%M-%S")+".csv"
#fileNameMaster = 'LUCY-DATE.csv'
DF=pd.DataFrame(master,columns=groupNameLegend) 
DF.to_csv(fileNameMaster)


class App(tk.Tk):
    def __init__(self):  
        super().__init__()
        #Window Builder
        self.title('Lucy Drop Tower')
        window_width = 1920-100
        window_height = 1080-200
        self.geometry(f'{window_width}x{window_height}')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()    
        #print(screen_height)
        #print(screen_width)
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        #self.eval('tk::PlaceWindow . center')
        #self.tk.call('tk', 'scaling', 1.5)

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


        #com=tk.StringVar(self)
        #com.set("COM1")
        #comSLCT=tk.OptionMenu(self.topSettingsFrame,com,'COM1','COM2','COM3','COM4')
        #comSLCT.grid(row = 0, column =0)
        #comShowbtnColor=tk.Button(self.topSettingsFrame,text='COM CHECK FUNCTION',font=fontButtons,command=self.fComUpdate)
        #comShowbtnColor.grid(row = 1, column =0)
        
        #Save/Load
        readbtnColor=tk.Button(self.topSettingsFrame,font=fontButtons,text="Load File", command=self.fLoad)
        readbtnColor.grid(row = 1, column =0)
        writebtnColor=tk.Button(self.topSettingsFrame,font=fontButtons,text="Save File", command=self.fSave)
        writebtnColor.grid(row = 1, column =1)

        superDropper=tk.Button(self.topSettingsFrame,font=fontGroups,text="Run Super Dropper", command=self.fSuperDropper)
        superDropper.grid(row = 3, column =0,sticky='ew',columnspan=2)

        # Top Run Frame
        self.topRunFrame = tk.Frame(self.topFrame)
        self.topRunFrame.config(background=topBG,pady=5,padx=5,highlightbackground=outline_color,highlightthickness=2)
        self.topRunFrame.grid(row = 0, column =1,sticky='news')
        self.topRunFrame.rowconfigure(0,weight = 1)
        self.topRunFrame.rowconfigure((0,1,2,3),weight = 1)
        self.topRunFrame.columnconfigure((0,1,2,3,4),weight = 1,uniform="foo")

        global readOut
        global var
        var = tk.StringVar()
        var.set("Waiting for Run")
        readOut = tk.Label(self.topRunFrame,textvariable=var,highlightthickness=1,highlightbackground=frame_color,background=topBG,font=fontHeader)
        readOut.grid(row = 2, column=1,sticky='ew',columnspan=3)

        global mainLab
        mainLab = tk.Label(self.topRunFrame,background=topBG,font=fontHeader)
        mainLab.grid(row = 0, column =0,sticky='ew',columnspan=5)
        rnbtnColor=tk.Button(self.topRunFrame,font=fontHeader,text="Run Dropper Function",background=btnColor,command=self.fDropper)
        rnbtnColor.grid(row = 1, column =0,sticky='ew',columnspan=5)
        
        self.trialSelection = tk.IntVar()
        tk.Radiobutton(self.topRunFrame,variable=self.trialSelection, value=0,command=self.fShow,indicatoron=0, selectcolor= btnColor_pressed,
                        text=' Trial 1 ', font=fontGroups, bg=btnColor,fg='black').grid(row = 2, column=0)
        tk.Radiobutton(self.topRunFrame,variable=self.trialSelection, value=1,command=self.fShow, indicatoron=0,selectcolor= btnColor_pressed,
                        text=' Trial 2 ',font=fontGroups, bg=btnColor,fg='black').grid(row = 2, column=4)

        
        # Top Finally Frame
        self.topMenuFrame = tk.Frame(self.topFrame)
        self.topMenuFrame.config(background=topBG,pady=5,padx=5,highlightbackground=outline_color,highlightthickness=2)
        self.topMenuFrame.grid(row = 0, column =2,sticky='news') 
        self.topMenuFrame.rowconfigure((0,1,2),weight = 1, uniform = 'a')
        self.topMenuFrame.columnconfigure(0,weight = 1)

        self.menuSelection = tk.IntVar()
        tk.Radiobutton(self.topMenuFrame,variable=self.menuSelection, value=0,command=self.fMenu1,indicatoron=0, selectcolor= btnColor_pressed,
                        text=' Show Single Group Graphs ', font=fontGroups, bg=btnColor,fg='black').grid(row = 0, column=0,stick='ew')
        tk.Radiobutton(self.topMenuFrame,variable=self.menuSelection, value=1,command=self.fMenu2,indicatoron=0, selectcolor= btnColor_pressed,
                        text=' Show All Graphs ',font=fontGroups,bg=btnColor,fg='black').grid(row = 1, column=0,stick='ew')
        tk.Radiobutton(self.topMenuFrame,variable=self.menuSelection, value=2,command=self.fMenu3,indicatoron=0, selectcolor= btnColor_pressed,
                        text=' Show Ranking ',font=fontGroups,bg=btnColor,fg='black').grid(row = 2, column=0,stick='ew')


        # SideBar Setup
        self.userSelection = tk.IntVar()
        for i in range(len(colorHex)):
            self.groupFrame=tk.Frame(self.sidebarFrame)
            self.groupFrame.config(bg=colorHex[i],pady=2,padx=2,highlightbackground=outline_color,highlightthickness=2)
            self.groupFrame.pack(expand = True , fill ='both')
            self.groupFrame.rowconfigure(0,weight = 1)
            self.groupFrame.columnconfigure((0),weight = 1)
            
            tk.Radiobutton(self.groupFrame,variable=self.userSelection, value=i,command=self.fShow, indicatoron=0, selectcolor= btnColor_pressed,
                            bg=btnColor,font=fontGroups,text = headerName[0][i],fg='black',padx=5,pady=5).grid(row = 0, column=0)

      

        # Main Menu Frames
        self.plotFrame = tk.Frame(self)
        self.plotFrame.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)

        fig = plt.Figure(facecolor=figure_color) 
        global ax
        ax = fig.subplots() 
        ax.cla()
        ax.set_xlabel(xAxis) 
        ax.set_ylabel(yAxis) 
        ax.grid()
        global graph
        graph = FigureCanvasTkAgg(fig, master=self.plotFrame) 
        graph.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        
        

        self.allFrame = tk.Frame(self)
        self.allFrame.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)

        allFig = plt.Figure(facecolor=figure_color) 
        global allAX
        allAX = allFig.subplots() 
        allAX.cla()
        allAX.set_xlabel(xAxis) 
        allAX.set_ylabel(yAxis) 
        allAX.grid()
        global allGraph
        allGraph = FigureCanvasTkAgg(allFig, master=self.allFrame) 
        allGraph.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        self.rankFrame = tk.Frame(self)
        self.rankFrame.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        
        rankFig = plt.Figure(facecolor=figure_color)
        global rankAX
        rankAX = rankFig.subplots()
        rankAX.cla()
        global rankGraph
        rankGraph = FigureCanvasTkAgg(rankFig, master=self.rankFrame) 
        rankGraph.get_tk_widget().pack(fill=tk.BOTH, expand=True)


        self.fShow()
        self.fMenu1()
        
    def fMenu1(self):
        self.plotFrame.tkraise()
    def fMenu2(self):
        self.allFrame.tkraise()
    def fMenu3(self):
        self.rankFrame.tkraise()
        
    def fDropper(self):
        trl=self.trialSelection.get()
        i = self.userSelection.get()
        self.fFileWriter(trl,i)
        data=pd.read_csv("data.csv")
        D=data.to_numpy()
        z=D[:,0]
        var.set("Processing")
        self.topSettingsFrame.update_idletasks()
        self.fSave(trl,i,z)

        self.fUpdater(trl,i,z)


        self.fShow()
        self.fShowAll()
        nameSorted,forceSorted,colorSorted= self.fSort()
        self.fRankShow(nameSorted,forceSorted,colorSorted)
        var.set("Waiting for Run")
        self.topSettingsFrame.update_idletasks()
    
    def fUpdater(self,trial,groupID,data):
        runForce[trial][groupID]=data/9.81
        runTime[trial][groupID]=np.linspace(0,5,len(data))
        maxForce[trial][groupID] = round(max(runForce[trial][groupID]).item(), 3)


    def fFileWriter(self,trial,groupID):
        f = open('data.csv','w',newline='')
        f.truncate()
        try:
            serialCom=serial.Serial(SERIAL_PORT,BAUD_RATE)
            serialCom.setDTR(False)
            time.sleep(.05)
            serialCom.flushInput()
            serialCom.setDTR(True)
            values = []
            for k in range(dropTime):
                try:
                    s_bytes=serialCom.readline()
                    decode_bytes = s_bytes.decode("utf-8").strip('\r\n')
                    #var.set(f'{round(k/dropTime*100)}'+'%')
                    if k==0:
                        var.set("Started - Data Capture")
                        values= decode_bytes.split(",")
                        self.topSettingsFrame.update_idletasks()
                    elif 0 < k/dropTime*100 <= 25:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('25%')
                        self.topSettingsFrame.update_idletasks()
                    
                    elif 25 < k/dropTime*100 <= 50:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('25%')
                        self.topSettingsFrame.update_idletasks()
                    
                    elif 50 < k/dropTime*100 <= 75:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('50%')
                        self.topSettingsFrame.update_idletasks()
                    
                    elif 75 < k/dropTime*100 <= 100:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('75%')
                        self.topSettingsFrame.update_idletasks()
                    else:
                        values = [float(x) for x in decode_bytes.split(",")]
                    writer = csv.writer(f,delimiter =',')
                    writer.writerow(values)
                except:
                    print("Error: Line was not recorded")
        except:
                print("Error: Line was not recorded")
        f.close()
        var.set("Stopped - Data Capture")

    def fFileWriterMAIN(self,trial,groupID):
        f = open('data.csv','w',newline='')
        #f.truncate()
        try:
            serialCom=serial.Serial(SERIAL_PORT,BAUD_RATE)
            serialCom.setDTR(False)
            time.sleep(.05)
            serialCom.flushInput()
            serialCom.setDTR(True)
            values = []
            for k in range(dropTime):
                try:
                    s_bytes=serialCom.readline()
                    decode_bytes = s_bytes.decode("utf-8").strip('\r\n')
                    #var.set(f'{round(k/dropTime*100)}'+'%')
                    if k==0:
                        var.set("Started - Data Capture")
                        values= decode_bytes.split(",")
                        self.topSettingsFrame.update_idletasks()
                    elif 0 < k/dropTime*100 <= 25:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('25%')
                        self.topSettingsFrame.update_idletasks()
                    
                    elif 25 < k/dropTime*100 <= 50:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('25%')
                        self.topSettingsFrame.update_idletasks()
                    
                    elif 50 < k/dropTime*100 <= 75:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('50%')
                        self.topSettingsFrame.update_idletasks()
                    
                    elif 75 < k/dropTime*100 <= 100:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('75%')
                        self.topSettingsFrame.update_idletasks()
                    else:
                        values = [float(x) for x in decode_bytes.split(",")]
                    writer = csv.writer(f,delimiter =',')
                    writer.writerow(values)
                except:
                    print("Error: Line was not recorded")
        except:
                print("Error: Line was not recorded")
        f.close()
        var.set("Stopped - Data Capture")
    
    def fFileWriter2(self):
        f = open('data1.csv','w',newline='')
        f.truncate()
        
        var.set("TEST")
        self.topSettingsFrame.update_idletasks()
        serialCom=serial.Serial(SERIAL_PORT,BAUD_RATE)
        serialCom.setDTR(False)
        time.sleep(.05)
        serialCom.flushInput()
        serialCom.setDTR(True)
        
        li=[]
        newli=[]
        var.set("Started - Data Capture")
        self.topSettingsFrame.update_idletasks()
        for i in range(dropTime):
            li+=[serialCom.readline()]

        var.set("Stopped - Data Capture")
        self.topSettingsFrame.update_idletasks()
        for i in li:
            try:
                decode_bytes=i.decode("utf-8").strip('\r\n')
                values = [float(x) for x in decode_bytes.split(",")]
            except:
                values=[0,0,0,0]
            newli+[values]
            writer = csv.writer(f,delimiter =',')
            writer.writerow(values)
        f.close()

    def fSuperDropper(self):
        
        for trl in range(2):
            for i in range(len(colorHex)):
                runTime[trl][i]=(np.arange(0, 20, 5))
                runForce[trl][i]=(np.random.normal(mu, sigma, len(runTime[trl][i])))
                maxForce[trl][i] = round(max(runForce[trl][i]).item(), 2)
                self.fShow()
                self.fShowAll()
                nameSorted,forceSorted,colorSorted= self.fSort()
                self.fRankShow(nameSorted,forceSorted,colorSorted)
    
    def fSort(self):
        maxForceLegend=maxForce[0]+maxForce[1]
        colorLegend= colorHex+colorHex
        groupNameSorted=[]
        maxForceSorted=[]
        colorSorted=[]
        rankNameSorted=[]
        for n in range(len(groupNameLegend)):
            if not maxForceLegend[n] ==0:
                groupNameSorted.append(groupNameLegend[n])
                maxForceSorted.append(maxForceLegend[n])
                colorSorted.append(colorLegend[n])
                rankNameSorted.append([])
        maxForceSorted,groupNameSorted,colorSorted =zip(*sorted(zip(maxForceSorted,groupNameSorted,colorSorted)))
        
        #print("---- RANKING ----")
        for m in range(len(groupNameSorted)):
                rankNameSorted[m]="#"+f'{m+1}'+" = " +f'{groupNameSorted[m]}'

        return rankNameSorted, maxForceSorted,colorSorted            
        
    def fHeaderUpdate(self,i):
        mainLab["text"]=headerName[1][i]
        self.headerFrame.configure(bg=colorHex[i])

    def fShow(self):
        trl=self.trialSelection.get()
        i = self.userSelection.get()
        self.fHeaderUpdate(i)
        ax.cla()
        ax.set_xlabel(xAxis) 
        ax.set_ylabel(yAxis) 
        ax.grid()
        ax.plot(runTime[0][i],runForce[0][i],color=colorHex[i])
        ax.plot(runTime[1][i],runForce[1][i],color=colorHex[i],linestyle='dashed')
        graph.draw() 
    
    def fShowAll(self):
        allAX.cla()
        allAX.set_xlabel(xAxis) 
        allAX.set_ylabel(yAxis) 
        allAX.grid()
        for i in range(len(colorHex)):
            allAX.plot(runTime[0][i],runForce[0][i],color=colorHex[i])
            allAX.plot(runTime[1][i],runForce[1][i],color=colorHex[i],linestyle='dashed')
        allGraph.draw()  

    def fRankShow(self,names,scores,color):
        rankAX.cla()


        low = min(scores)
        high = max(scores)

        #print(low)
        #print(high)

        for p in range(len(names)):
            rankAX.barh(names[p],scores[p],color=color[p])
        
        #rankAX.xlim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])

        rankAX.invert_yaxis()
        rankGraph.draw()


    def fLoad(self):
        var.set('LOAD SEQUENCE STARTED')
        self.topSettingsFrame.update_idletasks()

        filename = askopenfile(title = "Select file",filetypes = (("CSV Files","*.csv"),))    
        data=pd.read_csv(filename)
        master=data.to_numpy()
        #print(master[0,:])
        dropTime=len(master[:,0])+1

        #for trl in range(2):
        #    for i in range(len(colorHex)):
        #        loc=i+trl*i
        #        runForce[trl][i]=master[:,loc]/9.81
        #        runTime[trl][i]=np.linspace(0,5,len(runForce[trl][i]))
        #        maxForce[trl][i] = round(max(runForce[trl][i]).item(), 3)
        #        self.fShow()
        #        self.fShowAll()
        #        nameSorted,forceSorted,colorSorted= self.fSort()
        #        self.fRankShow(nameSorted,forceSorted,colorSorted)
        var.set('Waiting on Run')
        self.topSettingsFrame.update_idletasks()

    def fSave(self,trial,groupIndex,data):
        masterColumn=groupIndex+groupIndex*trial
        master[:,masterColumn]=data
        DF=pd.DataFrame(master,columns=groupNameLegend) 
        DF.to_csv(fileNameMaster)
        
        
    def fComUpdate(self):
        #SERIAL_PORT = str(com.get())
        print("Value Selected is: "+com.get())
        #print("Value of Serial Port STR is: "+SERIAL_PORT)
        #ser.port = SERIAL_PORT


    def fQuit(self):
        exit()


if __name__ == "__main__":
    app=App()
    app.mainloop()
    
    
