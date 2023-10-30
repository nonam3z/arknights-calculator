# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import math
import tkinter as tk

from data_parser.inventory import Inventory
from . import inventory_panels


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.controller = None

        self.frames = {}

        self.grid(padx=5, pady=5, sticky="nsew")

    def create_frames(self, inventory):
        for item in inventory:
            self.frames.setdefault(item, inventory_panels.InventoryPanels(self, item))

    def raise_frames(self):
        for frame in self.frames.values():
            frame.tkraise()

    def set_controller(self, controller):
        self.controller = controller

class Model:
    def __init__(self):
        pass

    @staticmethod
    def get_inventory():
        return Inventory().inventory.copy()


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def create_frames(self):
        self.clear_frames()
        inventory = self.model.get_inventory()
        self.view.create_frames(inventory)
        self.update_variables()
        self.clear_inventory()

    def parse_inventory(self):  # Парсим инвентарь, рассчитываем размеры для матрицы фреймов для отрисовки инвентаря.
        inventory = self.model.get_inventory()
        i = int(inventory.__len__())
        j = math.ceil(i / 7)
        return {'inv': inventory, 'i': i, 'j': j}

    def update_variables(self):
        m, n = 0, 0
        inv = self.parse_inventory()
        for c in range(7):
            self.view.columnconfigure(c, weight=1)
            for r in range(inv['j']):
                self.view.rowconfigure(r, weight=1)
        for itemFrame in self.view.frames.values():
            if itemFrame.view.itemId != "5001":
                itemFrame.view.grid(row=n, column=m, sticky="nsew")
                m = m + 1
                if m >= 7:
                    m, n = 0, (n + 1)

    def create_current_stash_list(self):
        data = {}
        for i in self.view.frames.values():
            data.setdefault(i.view.itemId, int(i.view.itemHave.get()))
        return data

    def clear_frames(self):
        self.view.frames = {}

    def clear_inventory(self):
        for frame in self.view.frames.values():
            frame.view.itemHave.set(0)
        return None

class InventoryFrame:
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.view = View(master=master)
        self.model = Model()
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)
        self.controller.create_frames()