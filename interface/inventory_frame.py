# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import math
import tkinter as tk
from tkinter import *

from PIL import Image, ImageTk

from data_parser.inventory import Inventory
from . import inventory_panels


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
        self.inv = self.parse_inventory()
        self.load_icons()
        self.update_variables()
        # self.raise_frames()

    @staticmethod
    def parse_inventory():  # Парсим инвентарь, рассчитываем размеры для матрицы фреймов для отрисовки инвентаря.
        inv = Inventory().inventory
        i = int(inv.__len__())
        j = math.ceil(i / 7)
        return {'inv': inv, 'i': i, 'j': j}

    def update_variables(self):
        m, n = 0, 0
        for c in range(7):
            self.columnconfigure(c, weight=1)
            for r in range(self.inv['j']):
                self.rowconfigure(r, weight=1)
        for itemFrame in InventoryFrame.frames.values():
            if itemFrame.itemId != "5001":
                itemFrame.grid(row=n, column=m, sticky="nsew")
                m = m + 1
                if m >= 7:
                    m, n = 0, (n + 1)

    def load_icons(self):
        for k in self.inv['inv'].values():
            item = inventory_panels.InvPanel(self)
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

    # def raise_frames(self):
    #     for frame in InventoryFrame.frames.values():
    #         frame.tkraise()

    @staticmethod
    def create_item_list():
        data = {}
        for i in InventoryFrame.frames.values():
            data.setdefault(i.itemId, int(i.itemHave.get()))
        return data
