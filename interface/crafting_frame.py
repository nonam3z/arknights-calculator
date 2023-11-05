# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import *
from tkinter import ttk

from data_parser.inventory import *


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.controller = None

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.text = StringVar()
        self.label = tk.Label(self, justify="left", textvariable=self.text)
        self.label.grid(column=0, row=0, sticky="ew")
        self.text.set("Total sanity cost: 0")

        self.craftingFrame = ttk.Treeview(self, columns=["name", "need"])
        self.craftingFrame.grid(column=0, row=1, sticky="nsew")
        self.craftingFrame.column("#0", stretch=False, width=150)
        self.craftingFrame.heading("#0", text="Icon", anchor="center")
        self.craftingFrame.column("name", stretch=True, width=150)
        self.craftingFrame.heading("name", text="Item", anchor="center")
        self.craftingFrame.column("need", stretch=True, width=50)
        self.craftingFrame.heading("need", text="Need to Craft", anchor="center")

    def set_controller(self, controller):
        self.controller = controller


class Model:
    def __init__(self):
        pass

    @staticmethod
    def get_inventory_data():
        return Inventory().inventory.copy()


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def clear_all(self):
        self.view.craftingFrame.delete(*self.view.craftingFrame.get_children())


class CraftingFrame:
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.view = View(master=master)
        self.model = Model()
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)

        #
        # def create_visible_tree(self, results):
        #     self.craftingFrame.delete(*self.craftingFrame.get_children())
        #     total_cost = 0
        #     results2 = results.copy()
        #     inventory = iFrame.InventoryFrame.create_item_list()
        #     for item in results:
        #         if results[item] <= inventory[item]:
        #             results2.pop(item)
        #         elif results[item] > inventory[item]:
        #             results2[item] = results2[item] - inventory[item]
        #     results = results2.copy()
        #     for item in results:
        #         lastIid = self.craftingFrame.insert("", tk.END, image=self.inventory[item].icon,
        #                                             values=(
        #                                                 self.inventory[item].name, results[item]))
        #     self.text.set("Total sanity cost: " + str(total_cost))
