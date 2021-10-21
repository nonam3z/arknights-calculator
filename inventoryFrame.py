import tkinter as tk
from tkinter import ttk
from tkinter import *
import ArknightsDataParser as ADP
import inventoryPanels
import PenguinLogisticsParser as PLP
import math
import mainWindow
from PIL import Image, ImageTk


inv = PLP.create_inventory()
PLP.calc_cost(inv)

i = int(inv.__len__())
j = math.ceil(i/6)

frames = {}


class InventoryFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(padx=5, pady=5, sticky="nsew")
        self.master = master

        for c in range(6):
            self.columnconfigure(c, weight=1)
            for r in range(j):
                self.rowconfigure(r, weight=1)

        for k in inv.values():
            item = inventoryPanels.InvPanel(self)
            item.itemId = k["itemId"]
            item.itemName.configure(text=k["name"], justify="right", anchor="e")
            item.itemHave.insert(0, "0")
            item.iconId = k["iconId"]
            item.icon = Image.open("items/" + k["iconId"] + ".png")
            item.icon.thumbnail((40, 40), Image.ANTIALIAS)
            # item.thumbnail = Image.open("items/" + k["iconId"] + ".png")
            # item.thumbnail.thumbnail((20, 20), Image.ANTIALIAS)
            item.imgIcon = ImageTk.PhotoImage(item.icon)
            item.itemIcon.create_image(10, 5, anchor="nw", image=item.imgIcon)
            # item.imgThumbnail = ImageTk.PhotoImage(item.thumbnail)
            # item.itemThumbnail.create_image(2, 2, anchor="nw", image=item.imgThumbnail)
            frames.setdefault(item.itemId)
            frames[item.itemId] = item

        n = 0
        m = 0

        for itemFrame in frames.values():
            itemFrame.grid(row=n, column=m, sticky="nsew")
            m = m + 1
            if m >= 6:
                n = n + 1
                m = 0

        for frame in frames.values():
            frame.tkraise()
