import tkinter as tk
from tkinter import ttk
from tkinter import *
import ArknightsDataParser as ADP
import inventoryPanels
import math
import mainWindow
from PIL import Image, ImageTk


def create_inventory():
    inv = ADP.inventory.items
    i = int(inv.__len__())
    j = math.ceil(i / 6)
    return {'inv': inv, 'i': i, 'j': j}


class InventoryFrame(tk.Frame):
    frames = {}

    def __init__(self, master=None):
        super().__init__(master)
        self.grid(padx=5, pady=5, sticky="nsew")
        self.master = master

        self.inv = create_inventory()

        for c in range(6):
            self.columnconfigure(c, weight=1)
            for r in range(self.inv['j']):
                self.rowconfigure(r, weight=1)

        for k in self.inv['inv'].values():
            item = inventoryPanels.InvPanel(self)
            item.itemId = k.itemId
            item.itemName.configure(text=k.name, justify="right", anchor="e")
            item.itemHave.insert(0, "0")
            item.iconId = k.iconId
            item.icon = Image.open("items/" + k.iconId + ".png")
            item.icon.thumbnail((40, 40), Image.ANTIALIAS)
            item.icon = ImageTk.PhotoImage(item.icon)
            item.itemIcon.create_image(10, 5, anchor="nw", image=item.icon)
            InventoryFrame.frames.setdefault(item.itemId)
            InventoryFrame.frames[item.itemId] = item

        n = 0
        m = 0

        for itemFrame in InventoryFrame.frames.values():
            if itemFrame.itemId != "5001":
                itemFrame.grid(row=n, column=m, sticky="nsew")
                m = m + 1
                if m >= 6:
                    n = n + 1
                    m = 0

        for frame in InventoryFrame.frames.values():
            frame.tkraise()
