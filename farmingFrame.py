import math
import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import ArknightsDataParser as ADP
import inventoryFrame as iFrame


class FarmingFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.item_list = {}
        self.inventory = ADP.Inventory().inventory

        self.text = StringVar()
        self.label = tk.Label(self, justify="left", textvariable=self.text)
        self.label.grid(column=0, row=0, sticky="ew")
        self.text.set("Total sanity cost: 0")

        self.bind("<FocusIn>", self.on_visibility)

        self.farmingFrame = ttk.Treeview(self, columns=["name", "need", "cost", "runs", "stage", "prob"])
        self.farmingFrame.grid(column=0, row=1, sticky="nsew")
        self.farmingFrame.column("#0", stretch=False, width=150)
        self.farmingFrame.heading("#0", text="Icon", anchor="center")
        self.farmingFrame.column("name", stretch=True, width=150)
        self.farmingFrame.heading("name", text="Item", anchor="center")
        self.farmingFrame.column("need", stretch=True, width=70)
        self.farmingFrame.heading("need", text="Need", anchor="center")
        self.farmingFrame.column("cost", stretch=True, width=70)
        self.farmingFrame.heading("cost", text="Cost (sum)", anchor="center")
        self.farmingFrame.column("runs", stretch=True, width=70)
        self.farmingFrame.heading("runs", text="Runs", anchor="center")
        self.farmingFrame.column("stage", stretch=True, width=150)
        self.farmingFrame.heading("stage", text="Stage", anchor="center")
        self.farmingFrame.column("prob", stretch=True, width=150)
        self.farmingFrame.heading("prob", text="Drop Chance", anchor="center")

        self.create_item_list()

    def create_item_list(self):
        """
        Создает список предметов с иконками для дальнейшей отрисовки таблицы.
        :return: Ничего не возвращает.
        """
        self.item_list = ADP.Inventory().inventory
        for item in self.item_list.values():
            try:
                icon = Image.open("items/" + item.iconId + ".png")
                icon.thumbnail((20, 20), Image.ANTIALIAS)
                icon = ImageTk.PhotoImage(icon)
                item.icon = icon
            except FileNotFoundError:
                print("File with id " + item.iconId + " not found, skipping...")
                item.icon = None
        return None

    def create_visible_tree(self, results):
        self.farmingFrame.delete(*self.farmingFrame.get_children())
        total_cost = 0
        results2 = results.copy()
        inventory = iFrame.InventoryFrame.create_item_list()
        for item in results:
            if results[item] <= inventory[item]:
                results2.pop(item)
            elif results[item] > inventory[item]:
                results2[item] = results2[item] - inventory[item]
        results = results2
        for item in results:
            stages = ADP.Database().stages
            stage = self.inventory[item].bestStageId
            if stage:
                runs = math.ceil((self.inventory[item].bestAp * results[item]) / stages[stage]["apCost"])
                cost = runs * stages[stage]["apCost"]
            else:
                runs = ""
                cost = ""
            lastIid = self.farmingFrame.insert("", tk.END, image=self.inventory[item].icon,
                                               values=(
                                                   self.inventory[item].name, results[item],
                                                   cost, runs, self.inventory[item].bestStage
                                               ))
        for item in self.farmingFrame.get_children():
            if self.farmingFrame.item(item)["values"][2]:
                total_cost += int(self.farmingFrame.item(item)["values"][2])
        self.text.set("Total sanity cost: " + str(total_cost))

    def on_visibility(self, event):
        self.master.planner.calculate()
        self.update()
