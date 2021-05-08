import tkinter as tk
from tkinter import ttk
from tkinter import *
import mainWindow


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Arknights Calculator")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        self.ear = 0
        self.earsListDict = {}

        master.minsize(width=1000, height=800)
        master.maxsize(width=1000, height=800)
        master.resizable(width=True, height=True)
        self.grid(padx=5, pady=5, sticky="nsew")

