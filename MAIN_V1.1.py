#!/usr/bin/env python3
__author__ = "Nicholas Rosato"
__copyright__ = "Copyright 2024, Collins Aerospace"
__credits__ = ["Nicholas Rosato","Stephen Kridel"]
__maintainer__ = "Nicholas Rosato"
__email__ = "nicholas.rosato@collins.com"


import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
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
yAxis="Force (LB)"
p_x = 0.09
p_y = 0.175 


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

headerName=[[],[]]
runTime=[[],[]]
runForce=[[],[]]
maxForce=[[],[]]
groupName = [[],[]]
peakForce=[[],[]]
deltaForce=[]

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
    peakForce[0].append([])
    peakForce[1].append([])
    deltaForce=[0].append(0)

runLength=len(colorHex)*trialNumber
mSlope=.0014
bZero=-1.80

trialTime=6.8
dropTime=5000
BAUD_RATE = 115200
SERIAL_PORT="COM4"

groupNameLegend=groupName[0]+groupName[1]
master=np.zeros(shape=(dropTime-1,runLength))
fileNameMaster=""
menuSelection=""



class menuAPP(tk.Tk):
    def __init__(self):  
        super().__init__()

        self.title('Lucy Drop Tower - File System')
        window_width = 480
        window_height = 240
        self.geometry(f'{window_width}x{window_height}')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()    
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

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
            self.resizable(False, False)


        self.fileFrame = tk.Frame(self)
        self.fileFrame.config(highlightbackground=outline_color,highlightthickness=1)
        self.fileFrame.pack(expand = True, fill ='both')
        self.fileFrame.rowconfigure(0,weight = 1,)
        self.fileFrame.columnconfigure(0,weight = 1,uniform='a')
        self.fileFrame.columnconfigure(1,weight = 1,uniform='a')
        
        NEWbtnColor=tk.Button(self.fileFrame,font=fontButtons,text="New File", command=self.fNewFile)
        NEWbtnColor.grid(row=0,column=0,sticky="nsew")
        LOADbtnColor=tk.Button(self.fileFrame,font=fontButtons,text="Load File", command=self.fLoad)
        LOADbtnColor.grid(row=0,column=1,sticky="nsew")
        
    def fLoad(self):
        global menuSelection
        menuSelection="LOAD"
        global fileNameMaster
        fileNameMaster = askopenfilename(title = "Select file",filetypes = (("CSV Files","*.csv"),))
        if fileNameMaster !="":
            print(str(fileNameMaster))
            DF=pd.read_csv(fileNameMaster)
            global master
            master=DF.to_numpy()
            print(fileNameMaster)
            self.destroy()
            self.fRunApp()


    def fNewFile(self):
        global menuSelection
        menuSelection="NEW"
        now = datetime.now()
        global fileNameMaster
        fileNameMaster = "LUCY-DATE-"+now.strftime("%d-%m-%Y")+"-TIME-"+now.strftime("%H-%M-%S")+".csv"
        DF=pd.DataFrame(master,columns=groupNameLegend) 
        DF.to_csv(fileNameMaster, index=False)
        print("File Created: " + fileNameMaster)
        self.destroy()
        self.fRunApp()


    def fRunApp(self):
        app=App()
        app.mainloop()



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
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

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
        self.bind("<Escape>", lambda command: quit())
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
        com=tk.StringVar(self)
        global readOut
        com.set(SERIAL_PORT)
        comOut = tk.Label(self.topSettingsFrame,textvariable=com,highlightthickness=1,highlightbackground=frame_color,background=topBG,font=fontHeader)
        comOut.grid(row = 0, column=0,sticky='ew')

        comShowbtnColor=tk.Button(self.topSettingsFrame,text='COM CHECK FUNCTION',font=fontButtons,command=self.fComUpdate)
        comShowbtnColor.grid(row = 0, column =1)


        testbtnColor=tk.Button(self.topSettingsFrame,text='TEST RUN',font=fontButtons,command=self.fTestRun)
        testbtnColor.grid(row = 2, column =1)
        #testbtnColor=tk.Button(self.topSettingsFrame,text='Clear Test',font=fontButtons,command=self.fCLEAR)
        #testbtnColor.grid(row = 2, column =0)


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
        rnbtnColor=tk.Button(self.topRunFrame,font=fontHeader,text="Run Dropper Function",background=btnColor,command=self.fRUN)
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

        # Plot Frames
        self.plotFrame = tk.Frame(self)
        
        self.plotFrame.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        self.plotFrameL = tk.Frame(self.plotFrame)
        self.plotFrameL.place(relx=0, rely=0, relwidth=.5, relheight=.8)
        self.plotFrameL.config(pady=2,padx=2,highlightbackground=outline_color,highlightthickness=1)
        self.plotFrameL.rowconfigure(0,weight = 1)
        self.plotFrameL.rowconfigure((0,1,2,3),weight = 1)
        self.plotFrameL.columnconfigure((0,1,2,3,4),weight = 1,uniform="foo")
        self.plotFrameR = tk.Frame(self.plotFrame)
        self.plotFrameR.place(relx=.5, rely=0, relwidth=.5, relheight=.8)
        self.plotFrameR.config(pady=2,padx=2,highlightbackground=outline_color,highlightthickness=1)
        
        # Bottom Frames
        self.bottomFrameL = tk.Frame(self.plotFrame)
        self.bottomFrameL.place(relx=0, rely=.8, relwidth=.5, relheight=.2)
        self.bottomFrameL.config(pady=2,padx=2,highlightbackground=outline_color,highlightthickness=1)
        self.bottomFrameL.rowconfigure((0,1,2),weight = 1, uniform = 'a')
        self.bottomFrameL.columnconfigure(0,weight = 1)
        self.bottomFrameR = tk.Frame(self.plotFrame)
        self.bottomFrameR.place(relx=.5, rely=.8, relwidth=.5, relheight=.2)
        self.bottomFrameR.config(pady=2,padx=2,highlightbackground=outline_color,highlightthickness=1)
        self.bottomFrameR.rowconfigure((0,1,2),weight = 1, uniform = 'a')
        self.bottomFrameR.columnconfigure(0,weight = 1)

        LHeadLab = tk.Label(self.bottomFrameL,font=fontHeader,text="Trial #1 Max Force")
        LHeadLab.grid(row = 0, column =0,sticky='news')
        global LForceLab
        LForceLab = tk.Label(self.bottomFrameL,font=fontHeader,text="#####")
        LForceLab.grid(row = 1, column =0,sticky='news')

        RHeadLab = tk.Label(self.bottomFrameR,font=fontHeader,text="Trial #2 Max Force")
        RHeadLab.grid(row = 0, column =0,sticky='news')
        global RForceLab
        RForceLab = tk.Label(self.bottomFrameR,font=fontHeader,text="#####")
        RForceLab.grid(row = 1, column =0,sticky='news')
        global RChangeLab
        RChangeLab = tk.Label(self.bottomFrameR,font=fontHeader,text="#####")
        RChangeLab.grid(row = 2, column =0,sticky='news')

        fig = plt.Figure(facecolor=figure_color) 
        global axL
        axL = fig.subplots() 
        axL.cla()
        axL.set_xlabel(xAxis) 
        axL.set_ylabel(yAxis) 
        axL.grid()
        global graphL
        graphL = FigureCanvasTkAgg(fig, master=self.plotFrameL) 
        graphL.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
                
        fig = plt.Figure(facecolor=figure_color) 
        global axR
        axR = fig.subplots() 
        axR.cla()
        axR.set_xlabel(xAxis) 
        axR.set_ylabel(yAxis) 
        axR.grid()
        global graphR
        graphR = FigureCanvasTkAgg(fig, master=self.plotFrameR) 
        graphR.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        self.rankFrame = tk.Frame(self)
        self.rankFrame.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        rankFig = plt.Figure(facecolor=figure_color)
        global rankAX
        rankAX = rankFig.subplots()
        rankAX.cla()
        global rankGraph
        rankGraph = FigureCanvasTkAgg(rankFig, master=self.rankFrame) 
        rankGraph.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.fHeaderUpdate(0)
        self.fMenu1()
        if menuSelection=="LOAD" and sum(master[0,:])!=0:
            self.fLoadUpdater()
            self.fShow()

        

    def fMenu1(self):
        self.plotFrame.tkraise()
        self.plotFrameL.tkraise()
        self.plotFrameR.tkraise()
        self.bottomFrameL.tkraise()
        self.bottomFrameR.tkraise()

    def fMenu2(self):
        print("fMenu2 Function Run")
    def fMenu3(self):
        self.rankFrame.tkraise()

    def fRUN(self):
        answer = askyesno(title='Confirmation', message='Are you sure that you want to run Dropper')
        if answer:
            self.fDropper()

    def fDropper(self):
        try:
            trl=self.trialSelection.get()
            i = self.userSelection.get()
            self.fFileWriter()
            var.set("Data Captured")
            self.topRunFrame.update_idletasks()
            data=pd.read_csv("data.csv")
            D=data.to_numpy()
            z=D[:,0]
            var.set("Processing")
            self.topRunFrame.update_idletasks()
            self.fSave(trl,i,z)
            var.set("Saved")
            self.topRunFrame.update_idletasks()
            self.fLoadUpdater()
            var.set("Waiting for Run")
            self.topRunFrame.update_idletasks()
        except:
            print("Error in Dropper")

    def fFileWriter(self):
        f = open('data.csv','w',newline='')
        f.truncate()
        try:
            serialCom=serial.Serial(SERIAL_PORT,BAUD_RATE)
            serialCom.setDTR(False)
            time.sleep(.05)
            serialCom.flushInput()
            serialCom.setDTR(True)
            values = []
            start_time = time.time()
            for k in range(dropTime):
                try:
                    s_bytes=serialCom.readline()
                    decode_bytes = s_bytes.decode("utf-8").strip('\r\n')
                    if k==0:
                        var.set("Started - Data Capture")
                        values= decode_bytes.split(",")
                        self.topRunFrame.update_idletasks()
                    elif 0 < k/dropTime*100 <= 25:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('0%')
                        self.topRunFrame.update_idletasks()
                    
                    elif 25 < k/dropTime*100 <= 50:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('25%')
                        self.topRunFrame.update_idletasks()
                    
                    elif 50 < k/dropTime*100 <= 75:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('50%')
                        self.topRunFrame.update_idletasks()
                    
                    elif 75 < k/dropTime*100 <= 100:
                        values = [float(x) for x in decode_bytes.split(",")]
                        var.set('75%')
                        self.topRunFrame.update_idletasks()
                    else:
                        values = [float(x) for x in decode_bytes.split(",")]
                    writer = csv.writer(f,delimiter =',')
                    writer.writerow(values)
                except:
                    print("Error: Line was not recorded")
        except:
                print("Error in Arduino")


        stop_time = time.time()
        delta_time=stop_time-start_time
        print(delta_time)
        f.close()
    

            

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
        
        for m in range(len(groupNameSorted)):
                rankNameSorted[m]="#"+f'{m+1}'+" = " +f'{groupNameSorted[m]}'

        return rankNameSorted, maxForceSorted,colorSorted            
        
    def fHeaderUpdate(self,i):
        mainLab["text"]=headerName[1][i]
        self.headerFrame.configure(bg=colorHex[i])

    def fShow(self):
        i = self.userSelection.get()
        self.fHeaderUpdate(i)
        graphMax=1.1*max(maxForce[0][i],maxForce[1][i])
        
        axL.cla()
        axL.set_xlabel(xAxis) 
        axL.set_ylabel(yAxis)
        axL.set_title("Trial 1")
        axL.grid()
        axL.plot(runTime[0][i],runForce[0][i],color=colorHex[i])
        axL.scatter(peakForce[0][i][0],peakForce[0][i][1],color="black")
        axL.set(ylim=(0,graphMax))
        graphL.draw() 

        axR.cla()
        axR.set_xlabel(xAxis) 
        axR.set_ylabel(yAxis) 
        axR.set_title("Trial 2")
        axR.grid()
        axR.plot(runTime[1][i],runForce[1][i],color=colorHex[i])
        axR.scatter(peakForce[1][i][0],peakForce[1][i][1],color="black")
        axR.set(ylim=(0,graphMax))
        graphR.draw() 
    
        L=round(peakForce[0][i][1],)
        LForceLab["text"]=f'{L} (LB)'
        self.bottomFrameL.update_idletasks()
        R=round(peakForce[1][i][1],1)
        RForceLab["text"]=f'{R} (LB)'

        if L !=0 and R !=0:
            try:
                #D=round(((R-L)/L)*100,1)
                D=round(R-L,1)
                
                if D<0:
                    RChangeLab["text"]=f'{abs(D)} (LB) Decrease'
                    RChangeLab["fg"]="green"
                if D>0:
                    RChangeLab["text"]=f'{abs(D)} (LB) Increase'
                    RChangeLab["fg"]="red"
            except:
                RChangeLab["text"]=f'{0}'
                RChangeLab["fg"]="black"
        else:
            RChangeLab["text"]=f'{0}'
            RChangeLab["fg"]="black"
        
        self.bottomFrameR.update_idletasks()

    def fRankShow(self,names,scores,color):
        rankAX.cla()

        low = min(scores)*.90
        high = max(scores)*1.1
        for p in range(len(names)):
            rankAX.barh(names[p],scores[p],color=color[p])
        
        for index, value in enumerate(scores):
            rankAX.text(value,index,str(value))
        
        rankAX.set_xlabel("Maximum " + yAxis) 
        rankAX.set(xlim=(low,high))
        rankAX.invert_yaxis()
        rankGraph.draw()

    def fLoadUpdater(self):
        for trl in range(2):
            for i in range(len(colorHex)):
                loc=i+(len(colorHex)*trl)
                if sum(master[:,loc])!=0.0:
                    runForce[trl][i]=((master[:,loc]*mSlope)+bZero)
                    #runForce[trl][i]=((master[:,loc]/gainMod)-gainAmp)*unitMod
                    runTime[trl][i]=np.linspace(0,trialTime,len(runForce[trl][i]))
                    maxForce[trl][i] = round(max(runForce[trl][i]).item(), 3)
                    y=max(runForce[trl][i])
                    x=np.average(runTime[trl][i][np.where(runForce[trl][i]==y)]).item()
                    peakForce[trl][i]=[x,y]
                else:
                    peakForce[trl][i]=[0,0]
               
        nameSorted,forceSorted,colorSorted= self.fSort()
        self.fRankShow(nameSorted,forceSorted,colorSorted)

    def fSave(self,trial,groupIndex,data):
        masterColumn=groupIndex+(len(colorHex)*trial)
        master[:,masterColumn]=data
        DF=pd.DataFrame(master,columns=groupNameLegend)
        DF.to_csv(fileNameMaster,mode='w',index=False)
        
    def fComUpdate(self):
        print(peakForce[0][0])
        print(peakForce[1][0])
        #try:
        #    ports = list_ports.comports()
        #    for port in ports: print(port)
        #    print(port[0])
        #except:     
        #    print("ComUpdate Error")

    def fQuit(self):
        exit()
    
    def fCLEAR(self):
        trl=self.trialSelection.get()
        i = self.userSelection.get()
        f = open('data.csv','w',newline='')
        f.truncate()
        for k in range(dropTime):
            writer = csv.writer(f,delimiter =',')
            writer.writerow([0])
        f.close()
        data=pd.read_csv("data.csv")
        D=data.to_numpy()
        z=D[:,0]
        self.fSave(trl,i,z)
        self.fLoadUpdater()
        var.set("Waiting for Run")
        self.topRunFrame.update_idletasks()

    def fZero0(self):
        try:
            f = open('zero.csv','w',newline='')
            f.truncate()
            serialCom=serial.Serial(SERIAL_PORT,BAUD_RATE)
            serialCom.setDTR(False)
            time.sleep(.05)
            serialCom.flushInput()
            serialCom.setDTR(True)
            values = []
            for k in range(100):
                try:
                    s_bytes=serialCom.readline()
                    decode_bytes = s_bytes.decode("utf-8").strip('\r\n')
                    values = [float(x) for x in decode_bytes.split(",")]
                    writer = csv.writer(f,delimiter =',')
                    writer.writerow(values)
                except:
                    print("Error: Line was not recorded")
            f.close()
        except:
            print('ZERO - Arduino FAILED')
        try:
            zeroData=pd.read_csv("zero.csv")
            D=zeroData.to_numpy()
            zeroAverage=np.average(D[:,0])
            print(zeroAverage)
        except:
            print('ZERO - AVERAGE FAILED')
    
    def fTestRun(self):
        try:
            self.fFileWriter()
            var.set("Data Captured")
            self.topRunFrame.update_idletasks()
            data=pd.read_csv("data.csv")
            D=data.to_numpy()
            z=((D[:,0]*mSlope)+bZero)
            #z=((D[:,0]/gainMod)-gainAmp)*unitMod
            TestForce=z
            TestTime=np.linspace(0,trialTime,len(TestForce))

            plt.plot(TestTime,TestForce)
            plt.ylabel(yAxis)
            plt.xlabel(xAxis)
            plt.show()
            var.set('Waiting on Run')
            self.topRunFrame.update_idletasks()
        except:
            print("TESTER FAIL")



if __name__ == "__main__":
    file=menuAPP()
    file.mainloop()
