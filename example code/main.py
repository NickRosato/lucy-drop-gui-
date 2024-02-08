import tkinter as tk

class Frame(): 
    ## no reason to inherit from Frame here
    def __init__(self, parent, num):
        self.parent=parent
        self.fr=tk.Frame(parent, padx=10, pady=10, bg="lightblue")

        tk.Label(self.fr, text="Label #%s" % (num+1)).grid()

class MainApp: 
    def __init__(self, root): 
        self.root = root

        # Create frames for each option
        self.frame_instances=[Frame(root, num) for num in range(4)]

        # Create the Start frame
        self.selection = tk.IntVar()
        self.start_frame = tk.Frame(root, padx=10, pady=10)
        self.start_frame.grid(row=0, column=0, sticky=tk.W)

        # Create Radiobuttons
        for btn in range(4):
            tk.Radiobutton(self.start_frame, text = "Button\n%s" % (btn+1), 
                          variable=self.selection, value=btn,
                          command=self.show_selected_frame, indicatoron=1
                          ).grid(row=btn, column=0)

        tk.Button(self.root, text="Quit", bg="orange",
                  command=self.root.quit).grid(row=20, column=0,
                  sticky="nsew")

        # Show the initially selected frame
        self.show_selected_frame()

    def show_selected_frame(self):
        # Reset frames
        for frame in self.frame_instances:
            frame.fr.grid_forget()

        selected_option = self.selection.get()
        print("selected", selected_option)
        self.frame_instances[selected_option].fr.grid(
                                       row=1, column=0)

if __name__ == "__main__": 
    root = tk.Tk() 
    app = MainApp(root) 
    root.mainloop()