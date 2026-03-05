import tkinter as tk

class BlankFrame(tk.Frame):
    def __init__(self, parent_frame: tk.Frame):
        tk.Frame.__init__(self, parent_frame)

        self.config(height=64, width=64)