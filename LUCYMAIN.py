import tkinter as tk
#import ttkbootstrap as tb


def create_main_window():
    root = tk.Tk()  
    root.title("Lucy Drop Tower")  
    root.geometry("1280x720")
    root.resizable(0, 0)
    #root.state('zoomed')

    p1 = tk.PhotoImage(file = 'info.png') 
    root.iconphoto(False, p1) 

    #label_header = tk.Label(root, text = "Lucy Drop Tower",font=('Arial', 35, 'bold'))# Create label for root window
    #label_header.pack()
  #spacer = tk.Label(root, text = "Lucy Drop Tower", font=('Arial', 10, 'bold')).grid(row=0,column=2)
    c1 = tk.Checkbutton(root, text="").grid(row=0,column=5)
    L1 = tk.Label(root, text="Display All",font=('Arial', 12,'bold')).grid(row=0,column=6)


    for x in range(2,14*2):
        if x % 2 ==0:
            L1 = tk.Label(root, text="Team Name:").grid(row=x,column=0)
            E1 = tk.Entry(root, bd =5).grid(row=x,column=1)
            ButtonRecord= tk.Button(root, text="Record",font=('Arial', 12),pady = 0,padx=0).grid(row=x,column=3)
            spacer = tk.Label(root,text="").grid(row=x,column=4)
            #ButtonDisplay= tk.Button(root, text="Display",font=('Arial', 12),pady = 0,padx=0).grid(row=x,column=5)
            c1 = tk.Checkbutton(root, text="").grid(row=x,column=5)
            L1 = tk.Label(root, text="Display",font=('Arial', 12)).grid(row=x,column=6)
        else:
            spacer = tk.Label(root,text="    ").grid(row=x,column=0)
   

    root.mainloop()# Display until closed manually

if __name__ == "__main__":
 create_main_window()
