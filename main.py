# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import *

import mainWindow


class App:
    def __init__(self):
        self.root = tk.Tk()
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        self.app = mainWindow.Application(master=self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.save_data)

    def save_data(self):
        self.app.save_data()
        self.app.save_settings()
        self.root.destroy()

    def start_program(self):
        self.app.mainloop()


if __name__ == "__main__":
    App().start_program()
