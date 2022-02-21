import tkinter as tk
from tkinter import ttk

import calculateFrame
import plannerFrame
import inventoryFrame as iFrame
import farmingFrame
import json
import os
import ArknightsDataParser

savedata = {}

if os.path.exists("savedata.json"):
    size = os.path.getsize("savedata.json")
    if size:
        savedata = json.load(open("savedata.json", encoding='utf-8'))


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.winfo_toplevel().title("Arknights Calculator")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        master.minsize(width=1200, height=900)
        master.maxsize(width=1200, height=900)
        master.resizable(width=True, height=True)
        self.grid(padx=5, pady=5, sticky="nsew")

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=0, column=0, sticky="nsew")
        self.planner = plannerFrame.Planner(self)
        self.tabs.add(self.planner, text="Planner")
        self.inventory = iFrame.InventoryFrame(self)
        self.tabs.add(self.inventory, text="Inventory Depot")
        self.calculator = calculateFrame.CalculateFrame(self)
        self.tabs.add(self.calculator, text="Path Calculator")
        # self.farming = farmingFrame.FarmingFrame(self)
        # self.tabs.add(self.farming, text="Farming Calculator")

    def restore_data(self):
        if savedata:
            for ear in savedata["earList"].values():
                name = ear["name"]
                iid = ear["iid"]
                sc = ear["current"]
                sd = ear["desired"]
                current = ArknightsDataParser.Stats(sc["elite"], sc["level"], sc["skill1"], sc["skill2"], sc["skill3"])
                desired = ArknightsDataParser.Stats(sd["elite"], sd["level"], sd["skill1"], sd["skill2"], sd["skill3"])
                operator = ArknightsDataParser.OperatorState(iid, name, current, desired)
                self.planner.allEarsList.setdefault(operator.name)
                self.planner.allEarsList[operator.name] = operator
                self.planner.earsList.insert("", tk.END,
                                             values=(name, self.planner.create_upgrade_string(current, desired)),
                                             iid=iid)
                # self.planner.create_path_list()
                self.calculator.update()
            for item in savedata["inventory"].values():
                iFrame.InventoryFrame.frames[item["itemId"]].itemHave.set(int(item["have"]))
