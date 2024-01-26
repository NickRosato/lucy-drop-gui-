#! /usr/bin/python3
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
  
"""
             
|               |              |
|               |              |
|               |              |
|               |              |
|-------------(x,y)------------|
|               |              |
|               |              |
|               |              |
|               |              |
              
"""




class TkinterApp(tk.Tk):
    """
     The class creates a header and sidebar for the application. Also creates
     two submenus in the sidebar, one for attendance overview with options to
     track students and modules, view poor attendance and another for
     database management, with options to update and add new modules to the
     database.
    """
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
        icon = tk.PhotoImage(file='info.png')
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
        """
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.85)
        submenu1 = SidebarSubMenu(self.submenu_frame,sub_menu_heading='SUBMENU 1',sub_menu_options=["Display Frame1","Display Frame2",])
        
        submenu1.options["Display Frame1"].config(command=lambda: self.show_frame(Frame1))
        submenu1.options["Display Frame2"].config(command=lambda: self.show_frame(Frame2))

        submenu1.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)
        """
        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground=frame_color, highlightthickness=1)
        container.place(relx=p_x, rely=p_y, relwidth=1-p_x, relheight=1-p_y)
        
        """
        self.frames = {}
        for F in (Frame1,Frame2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(Frame1)
        """

"""
    def show_frame(self, cont):
        
        #The function 'show_frame' is used to raise a specific frame (page) in
        #the tkinter application and update the title displayed in the header.

        #Parameters:
        #cont (str): The name of the frame/page to be displayed.
        #title (str): The title to be displayed in the header of the application.

        #Returns:
        #None
        
        frame = self.frames[cont]
        frame.tkraise()
"""

# ------------------------ MULTIPAGE FRAMES ------------------------------------


class Frame1(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Frame 1', font=("Arial", 15))
        label.pack()

"""
class Frame2(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Frame 2', font=("Arial", 15))
        label.pack()
"""

# ----------------------------- CUSTOM WIDGETS ---------------------------------
"""
class SidebarSubMenu(tk.Frame):
    
    #A submenu which can have multiple options and these can be linked with
    #functions.
    
    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        
        #parent: The frame where submenu is to be placed
        #sub_menu_heading: Heading for the options provided
        #sub_menu_operations: Options to be included in sub_menu
        
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(self,text=sub_menu_heading,bg=sidebar_color,fg="#333333",font=("Arial", 10))
        self.sub_menu_heading_label.place(x=30, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(self,text=x,bg=sidebar_color,font=("Arial", 9, "bold"),bd=0,cursor='hand2',activebackground='#ffffff',)
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")

"""
app = TkinterApp()
app.mainloop()