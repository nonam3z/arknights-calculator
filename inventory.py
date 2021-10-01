import tkinter as tk
from tkinter import ttk
from tkinter import *
import plannerPanels
import ArknightsDataParser
import json


class InventoryFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(padx=5, pady=5, sticky="nsew")
        self.master = master

        self.items = ArknightsDataParser.Item
        self.inventory = ArknightsDataParser.create_inventory(self)


        # self.selectElite = ttk.Spinbox(self, from_=0, to=2, command=self.callback)
        # self.selectElite.grid(column=1, row=0, sticky="ew")
        # self.selectElite.insert(0, "0")
