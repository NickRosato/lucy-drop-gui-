import tkinter as tk
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        
        self.title("Hello World")
        self.geometry("500x500")
        self.createWidgets()
        
        print(type(self))

        for item in dir(self):
            print(type(item),item)

    
    

    def createWidgets(self):

        t = np.arange(0, 3, .01)

        f0 = tk.Frame()
        
        fig = plt.figure(figsize=(8, 8))
        
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        canvas = FigureCanvasTkAgg(fig, f0)
        toolbar = NavigationToolbar2Tk(canvas, f0)
        toolbar.update()
        canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        
        
        f0.pack(fill=tk.BOTH, expand=1)

def main():
    appstart = GUI()
    appstart.mainloop()
    

if __name__ == "__main__":
    main()