import tkinter as tk
from tkinter import ttk
from tkinter import *

import inventoryFrame as iFrame
import plannerFrame
import plannerPanels
import ArknightsDataParser as ADP
import calculateFrame as cFrame
import win32clipboard
import json
import math
from PIL import Image, ImageTk


class FarmingFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.item_list = {}
        self.farming_list = {}

        self.button = tk.Button(self, text="Calculate Farming Route", command=self.create_path)
        self.button.grid(column=0, row=0, sticky="ew")

        self.farmingFrame = ttk.Treeview(self, columns=["name", "need", "have", "cost", "stage"])
        self.farmingFrame.grid(column=0, row=1, sticky="nsew")
        self.farmingFrame.column("#0", stretch=False, width=150)
        self.farmingFrame.heading("#0", text="Icon", anchor="center")
        self.farmingFrame.column("name", stretch=True, width=150)
        self.farmingFrame.heading("name", text="Item", anchor="center")
        self.farmingFrame.column("need", stretch=True, width=70)
        self.farmingFrame.heading("need", text="Need", anchor="center")
        self.farmingFrame.column("have", stretch=True, width=70)
        self.farmingFrame.heading("have", text="Have", anchor="center")
        self.farmingFrame.column("cost", stretch=True, width=70)
        self.farmingFrame.heading("cost", text="Cost", anchor="center")
        self.farmingFrame.column("stage", stretch=True, width=150)
        self.farmingFrame.heading("stage", text="Stage", anchor="center")

    def create_item_list(self):
        self.item_list = ADP.inventory.items
        for item in self.item_list.values():
            icon = Image.open("items/" + item.iconId + ".png")
            icon.thumbnail((20, 20), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(icon)
            item.icon = icon
            item.have = iFrame.InventoryFrame.frames[item.itemId].itemHave.get()
        return None

    def create_path(self):
        results = cFrame.CalculateFrame.call_farming_data()
        if results:
            for item in results:
                self.farmingFrame.insert("", tk.END, image=self.item_list[item].icon,
                                         values=(
                                           self.item_list[item].name, results[item], self.item_list[item].have,
                                           self.item_list[item].bestAp * results[item],
                                           self.item_list[item].bestStage))
