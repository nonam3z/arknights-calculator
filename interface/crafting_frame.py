# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import *
from tkinter import ttk


class CraftingFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.item_list = {}

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


class Controller:
    def __init__(self):
        pass

        # self.inventory = ADP.Inventory().inventory
        # self.create_item_list()
        #
        # def create_item_list(self):
        #     """
        #     Создает список предметов с иконками для дальнейшей отрисовки таблицы.
        #     :return: Ничего не возвращает.
        #     """
        #     self.item_list = ADP.Inventory().inventory
        #     for item in self.item_list.values():
        #         try:
        #             icon = Image.open("items/" + item.iconId + ".png")
        #             icon.thumbnail((20, 20), Image.ANTIALIAS)
        #             icon = ImageTk.PhotoImage(icon)
        #             item.icon = icon
        #         except FileNotFoundError:
        #             print("File with id " + item.iconId + " not found, skipping...")
        #             item.icon = None
        #     return None
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
        #
        # def on_visibility(self, event):
        #     self.master.planner.calculate()
        #     self.update()
        #
        # def clear_all(self):
        #     self.craftingFrame.delete(*self.craftingFrame.get_children())
