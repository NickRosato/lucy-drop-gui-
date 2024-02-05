#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import sys
#import serial
#import io


main_color = 'white'
header_color = '#E61231'
visualisation_frame_color = "#ffffff"
sidebar_color = "white"
outline_color = '#808080'
frame_color = 'grey'
#Shape Builder RELXY
p_x = 0.15
p_y = 0.05  
#filepath = "/home/LucyDropTower/Documents/lucy-drop-gui-/"

GROUPS=['DeepPink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Magenta','Purple','Navy','Grey','Black']


class App(tk.Tk):
    def __init__(self,title,size):
        
        #main setup
        super().__init__()
        #self.attributes('-zoomed', True)
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.attributes('-fullscreen',True)
        self.bind("<Escape>", lambda event: self.quit())
        self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))


        #widgets
        self.sidebar = Sidebar(self)
        self.header = Header(self)
        self.main = Main(self)

 
        #run app
        self.mainloop()

class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(highlightbackground=outline_color,highlightthickness=1)
        self.place(relx=0, rely=p_y, relwidth=p_x, relheight=1)
    
        
        for x in range(len(GROUPS)):
            Segment(self,'Group: '+f'{x+1}',GROUPS[x],x)

        RankingButton = tk.Button(self,text = "Ranking",fg='black').pack(expand = False, fill ='both')

        FinalyButton = tk.Button(self,text = "Finaly Showcase",fg='black').pack(expand = False, fill ='both')
class Segment(tk.Frame):
    def __init__(self, parent,label_text,color,order):
        super().__init__(parent)
        self.config(background = color,pady=7.5)

        #grid layout
        self.rowconfigure(0,weight = 0)
        self.columnconfigure((0,1,2),weight = 1,uniform='a')
        
        tk.Label(self,bg='white',font=("Arial", 12, "bold"),text = label_text).grid(row = 0, column =0)
        tk.Button(self,text = "Run",fg='black').grid(row = 0, column=1)
        tk.Checkbutton(self,bg = 'white',fg='black').grid(row = 0, column = 2)
        
        self.pack(expand = False, fill ='both')

class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(background=header_color,highlightbackground=outline_color,highlightthickness=1,padx = 20)
        self.place(relx=0, rely=0, relwidth=1, relheight=p_y)
        
        title=tk.Label(self,text='Lucy Drop Tower',bg=header_color,font=("Arial", 15, "bold"))
        title.pack(side=tk.LEFT)      
        close = tk.Button(self,text='X',background=sidebar_color,font=("Arial", 15, "bold"),command = self.quit)
        close.pack(side=tk.RIGHT)      

class Main(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg=main_color,highlightbackground=outline_color,highlightthickness=1)
        self.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)



App('Lucy Drop Tower',(1600,1000))