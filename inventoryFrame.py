import math
import tkinter as tk
from tkinter import *

from PIL import Image, ImageTk

import ArknightsDataParser as ADP
import inventoryPanels


def parse_inventory():  # Парсим инвентарь, рассчитываем размеры для матрицы фреймов для отрисовки инвентаря.
    inv = ADP.Inventory().inventory
    i = int(inv.__len__())
    j = math.ceil(i / 7)
    return {'inv': inv, 'i': i, 'j': j}


class InventoryFrame(tk.Frame):
    frames = {}

    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.master = master

        self.inv = None
        self.update_inventory()

    @staticmethod
    def clear_inventory():
        for frame in InventoryFrame.frames.values():
            frame.itemHave.set(0)
        return None

    def update_inventory(self):

        InventoryFrame.frames = {}

        for child in InventoryFrame.winfo_children(self):
            child.destroy()

        self.inv = parse_inventory()

        for c in range(7):
            self.columnconfigure(c, weight=1)
            for r in range(self.inv['j']):
                self.rowconfigure(r, weight=1)

        for k in self.inv['inv'].values():
            item = inventoryPanels.InvPanel(self)
            item.itemId = k.itemId
            item.itemName.configure(text=k.name, justify="right", anchor="e")
            item.itemHave.insert(0, "0")
            item.iconId = k.iconId
            InventoryFrame.frames.setdefault(item.itemId)
            InventoryFrame.frames[item.itemId] = item
            try:
                item.icon = Image.open("items/" + k.iconId + ".png")
                item.icon.thumbnail((40, 40), Image.ANTIALIAS)
                item.icon = ImageTk.PhotoImage(item.icon)
                item.itemIcon.create_image(10, 5, anchor="nw", image=item.icon)
            except FileNotFoundError:
                print("File with id " + item.iconId + " not found, skipping...")
                item.icon = None

        n = 0
        m = 0

        for itemFrame in InventoryFrame.frames.values():
            if itemFrame.itemId != "5001":
                itemFrame.grid(row=n, column=m, sticky="nsew")
                m = m + 1
                if m >= 7:
                    n = n + 1
                    m = 0

        for frame in InventoryFrame.frames.values():
            frame.tkraise()

    @staticmethod
    def create_item_list():
        data = {}
        for i in InventoryFrame.frames.values():
            data.setdefault(i.itemId, int(i.itemHave.get()))
        return data
