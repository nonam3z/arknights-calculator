import tkinter as tk
from tkinter import ttk
from tkinter import *

import inventoryFrame
import plannerPanels
import ArknightsDataParser
import win32clipboard
import json
import math
from PIL import Image, ImageTk


class CalculateFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.master = master

        self.calculateFrame = ttk.Treeview(self, show="headings", columns=["name", "need", "have", "cost", "stage"])
        self.results.grid(column=0, row=0, sticky="nsew")


