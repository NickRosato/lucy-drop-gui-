#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
import sys
from sys import platform
import matplotlib.pyplot as plt
import numpy as np

main_color = 'white'
header_color = '#E61231'
sidebar_color = "white"
outline_color = '#808080'
frame_color = 'grey'
fontHeader=("Arial", 15, "bold")
fontGroups=("Arial", 12, "bold")
fontButtons=("Arial", 10, "bold")
p_x = 0.15 # for 1920 : x = 288
p_y = 0.025  # for 1080 : y = 27

groupColor=['DeepPink','Red','Coral','Orange','Gold','Chartreuse','Green','Turquoise','Blue','Magenta','Purple','Navy','Grey','Black']
groups=[]
btnName=[]
for index in range(len(groupColor)):
    groups.append('Group: '+f'{index+1}')
    btnName.append('Display Group: '+f'{index+1}')


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
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

        self.bind("<Escape>", lambda event: exit())




        self.header = tk.Frame(self)
        self.header.config(background=header_color,highlightbackground=outline_color,highlightthickness=1,padx = 20)
        self.header.place(relx=0, rely=0, relwidth=1, relheight=p_y)


        self.sidebarTP = tk.Frame(self)
        self.sidebarTP.config(highlightbackground=outline_color,highlightthickness=1,pady=5,padx=5)
        self.sidebarTP.place(relx=0, rely=p_y, relwidth=p_x, relheight=.85)

        self.main = tk.Frame(self)
        self.main.configure(bg=main_color,highlightbackground=outline_color,highlightthickness=1)
        self.main.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        

        # # SUBMENU 1
        #self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        #self.submenu_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.85)
        
        submenu = SidebarSubMenu(self.sidebarTP,sub_menu_heading='SUBMENU',sub_menu_options=btnName,color_option=groupColor)
        
        submenu.options[btnName[0]].config(command=lambda: self.show_frame(Frame1))
        submenu.options[btnName[1]].config(command=lambda: self.show_frame(Frame2))
        submenu.options[btnName[2]].config(command=lambda: self.show_frame(Frame1))
        submenu.options[btnName[3]].config(command=lambda: self.show_frame(Frame2))
        submenu.options[btnName[4]].config(command=lambda: self.show_frame(Frame2))

        submenu.place(relx=0, rely=0, relwidth=1,relheight=1)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        #container = tk.Frame(self)
        #container.config(highlightbackground="#808080", highlightthickness=0.5)
        #container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.frames = {}

        for F in (Frame1,Frame2):
            frame = F(self.main, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(Frame1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        




class Frame1(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Frame 1', font=("Arial", 15))
        label.pack()


class Frame2(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.configure(background=groupColor[2])

        label = tk.Label(self, text='Frame 2', font=("Arial", 15))
        label.pack()



class SidebarSubMenu(tk.Frame):
    def __init__(self, parent, sub_menu_heading, sub_menu_options,color_option):
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        #self.sub_menu_heading_label = tk.Label(self,text=sub_menu_heading,bg=sidebar_color,fg="#333333",font=("Arial", 10))
        #self.sub_menu_heading_label.place(x=30, y=10, anchor="w")
        #sub_menu_sep = ttk.Separator(self, orient='horizontal')
        #sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")
        #color = groupColor[index]
        #labelText = 'Group: '+f'{index+1}'
        #self.config(background = color,pady=10,padx=5)

        #grid layout
        self.rowconfigure(0,weight = 0)
        self.columnconfigure((0,1),weight = 1,uniform='a')


        self.options = {}
        self.left = {}
        for n, x in enumerate(sub_menu_options):
            #self.left[x]=tk.Label(self,bg='white',font=fontGroups,text = labelText,highlightbackground=outline_color,highlightthickness=1.5)
            #self.left[x].grid(row = n, column =0)
            self.options[x] = tk.Button(self,text=x,font=fontButtons,bg="white",bd=0,cursor='hand2',activebackground='#ffffff',)
            self.options[x].grid(row = n, column=1)


app = App()
app.mainloop()