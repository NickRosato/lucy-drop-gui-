#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = 'white'
sidebar_color = 'white'
header_color = '#E61231'
visualisation_frame_color = "#ffffff"
frame_color = "#808080"
# ------------------------------- ROOT WINDOW ----------------------------------

#Shape Builder
p_x = 0.15
p_y = 0.05  



class TkinterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Lucy Drop Tower")

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1600x1000")
        self.attributes('-fullscreen', True)
        #self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.bind("<Escape>", lambda event: self.quit())
        #self.attributes("-fullscreen", False)

        self.title('Lucy Drop Tower')
        #self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file='/home/LucyDropTower/Documents/lucy-drop-gui-/info.png')
        self.iconphoto(True, icon)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=p_x, rely=0, relwidth=1-p_x, relheight=p_y)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=p_x, relheight=1)

        # LOGO AND NAME
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color, highlightthickness=1)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=p_y)
        self.uni_logo = icon.subsample(5)
        logo = tk.Label(self.brand_frame, image=self.uni_logo, bg=sidebar_color)
        logo.place(relx=0, rely=0)     
        name = tk.Label(self.brand_frame,text='Lucy Drop Tower',bg=sidebar_color,font=("", 15, "bold"))
        name.place(relx=.25, rely=.5, anchor="w")

        # SUBMENUS IN SIDE BAR

        # # SUBMENU 1
        
        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground=frame_color, highlightthickness=1)
        container.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        

# ------------------------ MULTIPAGE FRAMES ------------------------------------


class Frame1(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Frame 1', font=("Arial", 15))
        label.pack()



app = TkinterApp()
app.mainloop()