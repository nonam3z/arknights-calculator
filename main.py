import interfaceInit
import tkinter as tk
from tkinter import *


root = tk.Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
app = interfaceInit.Application(master=root)
root.protocol("WM_DELETE_WINDOW", root.destroy)
app.mainloop()
