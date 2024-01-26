#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk


selectionbar_color = 'white'
sidebar_color = 'white'
header_color = '#E61231'
visualisation_frame_color = "#ffffff"
frame_color = "#808080"

#Shape Builder RELXY
p_x = 0.15
p_y = 0.05  
filepath = "/home/LucyDropTower/Documents/lucy-drop-gui-/"


class TkinterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Lucy Drop Tower")
        #self.geometry("1600x1000")
        self.attributes('-fullscreen', True)
        #self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.bind("<Escape>", lambda event: self.quit())
        #self.attributes("-fullscreen", False)

        #HEADER FRAME CREATE
        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=p_x, rely=0, relwidth=1-p_x, relheight=p_y)
        tk.Button(self.header,text='X',bg=sidebar_color,font=("Arial", 15, "bold"),command = self.destroy).place(relx=.97, rely=.5, anchor="w")

        #SIDEBAR FRAME CREATE
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=p_x, relheight=1)

        #SIDEBAR - LOGO
        icon = tk.PhotoImage(file= filepath +'info.png')
        self.iconphoto(True, icon)
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color, highlightthickness=1)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=p_y)
        self.logo = icon.subsample(5)
        tk.Label(self.brand_frame, image=self.logo, bg=sidebar_color).place(relx=0, rely=0)     
        tk.Label(self.brand_frame,text='Lucy Drop Tower',bg=sidebar_color,font=("Arial", 15, "bold")).place(relx=.25, rely=.5, anchor="w")

        #MAIN FRAME CREATE
        main = tk.Frame(self)
        main.config(highlightbackground=frame_color, highlightthickness=1)
        main.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)

app = TkinterApp()
app.mainloop()