import math
import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import ArknightsDataParser as ADP
import inventoryFrame as iFrame


class CalculateFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.inventory = ADP.Inventory().inventory
        self.farming_data = {}
        self.crafting_data = {}
        self.inventory_copy = {}
        self.item_list = {}

        self.text = StringVar()
        self.label = tk.Label(self, justify="left", textvariable=self.text)
        self.label.grid(column=0, row=0, sticky="ew")
        self.text.set("Total items sanity cost: 0")

        self.bind("<FocusIn>", self.on_visibility)

        self.calculateFrame = ttk.Treeview(self, columns=["name", "need", "cost", "runs", "stage"])
        self.calculateFrame.grid(column=0, row=1, sticky="nsew")
        self.calculateFrame.column("#0", stretch=False, width=150)
        self.calculateFrame.heading("#0", text="Icon", anchor="center")
        self.calculateFrame.column("name", stretch=True, width=150)
        self.calculateFrame.heading("name", text="Item", anchor="center")
        self.calculateFrame.column("need", stretch=True, width=70)
        self.calculateFrame.heading("need", text="Need", anchor="center")
        self.calculateFrame.column("cost", stretch=True, width=70)
        self.calculateFrame.heading("cost", text="Cost (sum)", anchor="center")
        self.calculateFrame.column("runs", stretch=True, width=70)
        self.calculateFrame.heading("runs", text="Runs", anchor="center")
        self.calculateFrame.column("stage", stretch=True, width=150)
        self.calculateFrame.heading("stage", text="Stage", anchor="center")
        self.calculateFrame.tag_configure('comp', background='Yellow')
        self.calculateFrame.tag_configure('farm', background='Red')

        self.create_item_list()

    def create_item_list(self):
        """
        Создает список предметов с иконками для дальнейшей отрисовки таблицы.
        :return: Ничего не возвращает.
        """
        for item in self.inventory.values():
            try:
                icon = Image.open("items/" + item.iconId + ".png")
                icon.thumbnail((20, 20), Image.ANTIALIAS)
                icon = ImageTk.PhotoImage(icon)
                item.icon = icon
            except FileNotFoundError:
                print("File with id " + item.iconId + " not found, skipping...")
                item.icon = None

    def create_results_dict(self, results):
        inventory = iFrame.InventoryFrame.create_item_list()
        results2 = results.copy()
        for item in results:
            if results[item]["need"] <= inventory[item] > 0:
                results2.pop(item)
            elif results[item]["need"] > inventory[item]:
                results2[item]["need"] = results2[item]["need"] - inventory[item]
        results = results2
        for item in results:
            results[item]["formulas"] = self.create_materials_tree(item, results[item]["need"])
        return results

    def create_materials_tree(self, itemId, need):
        chips_id = ["3212", "3222", "3232", "3242", "3252", "3262", "3272", "3282"]
        small_chips_id = ["3211", "3221", "3231", "3241", "3251", "3261", "3271", "3281"]
        results = {}
        if itemId not in chips_id:
            if itemId not in small_chips_id:
                if ADP.Inventory().inventory[itemId].formula:
                    materials = ADP.Inventory().inventory[itemId].formula["costs"]
                    for m in materials:
                        results.setdefault(m["id"], ({"itemId": m["id"], "need": need * m["count"],
                                                      "formulas": {}}))
                        if ADP.Inventory().inventory[m["id"]].formula:
                            results[m["id"]]["formulas"] = self.create_materials_tree(m["id"], results[m["id"]]["need"])
            return results
        else:
            return results

    def create_visible_tree(self, results):
        self.calculateFrame.delete(*self.calculateFrame.get_children())
        self.farming_data = {}
        self.crafting_data = {}
        results = self.create_results_dict(results)
        total_cost = 0
        for item in results:
            self.create_branch(results[item], "")
        for item in self.calculateFrame.get_children():
            if self.calculateFrame.item(item)["values"][2]:
                total_cost += int(self.calculateFrame.item(item)["values"][2])
        self.master.farming.create_visible_tree(self.farming_data)
        self.master.crafting.create_visible_tree(self.crafting_data)
        self.text.set("Total item sanity cost: " + str(total_cost))

    def create_branch(self, item, iid):
        stages = ADP.Database().stages
        stage = self.inventory[item["itemId"]].bestStageId
        if stage:
            runs = math.ceil((self.inventory[item["itemId"]].bestAp * item["need"]) / stages[stage]["apCost"])
            cost = runs * stages[stage]["apCost"]
        else:
            runs = ""
            cost = ""
        lastIid = self.calculateFrame.insert(iid, tk.END, image=self.inventory[item["itemId"]].icon,
                                             values=(
                                                 self.inventory[item["itemId"]].name, item["need"],
                                                 cost, runs, self.inventory[item["itemId"]].bestStage
                                             ))
        if self.inventory[item["itemId"]].flags == "Farming":
            if self.farming_data.get(item["itemId"]):
                self.farming_data[item["itemId"]] = self.farming_data[item["itemId"]] + item["need"]
            else:
                self.farming_data.setdefault(item["itemId"], item["need"])
        if self.inventory[item["itemId"]].flags == "Crafting":
            if self.crafting_data.get(item["itemId"]):
                self.crafting_data[item["itemId"]] = self.crafting_data[item["itemId"]] + item["need"]
            else:
                self.crafting_data.setdefault(item["itemId"], item["need"])
            if item["formulas"]:
                for mat in item["formulas"]:
                    self.create_branch(item["formulas"][mat], lastIid)

    def on_visibility(self, event):
        self.master.planner.calculate()
        self.update()
