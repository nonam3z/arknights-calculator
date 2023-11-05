# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import ttk

from data_parser.inventory import Inventory


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.controller = None

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.itemId = None

        self.itemIcon = tk.Canvas(self, width=50, height=50)
        self.itemIcon.grid(row=1, column=0, sticky="nsew")

        self.itemName = tk.Label(self, width=180)
        self.itemName.grid(row=0, column=0, columnspan=2)

        self.itemHave = ttk.Spinbox(self, from_=0, to=999999999, values=["0"])
        self.itemHave.grid(row=1, column=1)

    def set_controller(self, controller):
        self.controller = controller


class Model:
    def __init__(self):
        pass

    @staticmethod
    def get_inventory_data():
        return Inventory().inventory.copy()


class ValidateModel:
    def __init__(self, view):
        self.view = view

        self.vcmd = (self.view.register(self.validateInv))
        self.ivcmd = (self.view.register(self.onInvalid))

    def set_validate(self):
        self.view.itemHave.configure(validate="key", validatecommand=self.vcmd, invalidcommand=self.ivcmd)

    def validateInv(self, P, W):
        widget = self.view.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        try:
            if P == "":
                return True
            if P.isdigit():
                if _from <= int(P) <= _to:
                    return True
        except ValueError:
            return False
        return False

    def onInvalid(self, W, P):
        widget = self.view.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        widget.delete(0, 99)
        try:
            if P.isdigit():
                if int(P) >= _to:
                    widget.insert(0, _to)
                if int(P) <= _from:
                    widget.insert(0, _from)
            else:
                widget.insert(0, _from)
        except ValueError:
            widget.insert(0, _from)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_data(self, itemId):
        inventory = self.model.get_inventory_data()
        self.view.itemName.configure(text=inventory[itemId].name, justify="right", anchor="e")
        try:
            self.view.itemIcon.create_image(10, 5, anchor="nw", image=inventory[itemId].iconMedium)
        except FileNotFoundError:
            print(f"There is no icon {self.view.iconId} in inventory data, skipping...")

class InventoryPanels:
    def __init__(self, master, itemId):
        super().__init__()

        self.master = master

        self.view = View(master=master)
        self.model = Model()
        self.validate = ValidateModel(self.view)
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)
        self.validate.set_validate()

        self.view.itemId = itemId
        self.controller.load_data(itemId)