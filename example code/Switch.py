from tkinter import *
fenster = Tk()
fenster.title("Window")

def switch():
    b1.config(state=DISABLED)

#--Buttons
b1=Button(fenster, text="Button")
b1.config(height = 5, width = 7)
b1.grid(row=0, column=0)    

b2 = Button(text="disable", command=switch)
b2.grid(row=0,column=1)

fenster.mainloop()
