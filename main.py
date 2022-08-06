import tkinter as tk
from tkinter import *

import mainWindow


def save_data():
    app.save_data()
    app.save_settings()
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    app = mainWindow.Application(master=root)
    root.protocol("WM_DELETE_WINDOW", save_data)
    app.mainloop()
