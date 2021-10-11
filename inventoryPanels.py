import tkinter as tk
from tkinter import ttk
import json
import ArknightsDataParser as ADP
from urllib.request import urlretrieve
import os

# repository = "https://penguin-stats.io/PenguinStats/api/v2/result/matrix?show_closed_zones=false&server=US"
# file = "materials.json"
# os.remove(file)
# open(file, 'w+')
# urlretrieve(repository, file)

mats = json.load(open("materials.json", encoding='utf-8'))
mats = mats["matrix"]
stages = json.load(open("jsons/stage_table.json", encoding='utf-8'))
stages = stages["stages"]


def create_inventory():
    inventory = {}
    for itemList in ADP.items["items"].values():
        if itemList["classifyType"] == "MATERIAL" and itemList["itemType"] == "MATERIAL" and not itemList["obtainApproach"]:
            inventory[itemList["itemId"]] = itemList
            inventory[itemList["itemId"]]["stages"] = {}
    for i in range(len(mats)):
        count = mats[i]
        for items in inventory.values():
            if count["itemId"] == items["itemId"]:
                inventory[count["itemId"]]["stages"][count["stageId"]] = count
        None
    None
    return inventory


def calc_cost(inv):
    for items in inv.values():
        for i in items["stages"].values():
            perRun = float(i["quantity"])/float(i["times"])
            if stages.get(i["stageId"]):
                apCost = stages[i["stageId"]]["apCost"]
            else:
                apCost = 1000
            inv[i["itemId"]]["stages"][i["stageId"]]["perRun"] = perRun
            inv[i["itemId"]]["stages"][i["stageId"]]["apCost"] = apCost
            if perRun > 0:
                inv[i["itemId"]]["stages"][i["stageId"]]["costPerItem"] = apCost/perRun
            else:
                inv[i["itemId"]]["stages"][i["stageId"]]["costPerItem"] = 1000
            None
        None
    return None


class InvPanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)

        self.itemId = ""
        self.imgIcon = ""
        self.coos = ""

        self.itemIcon = tk.Canvas(self, width=50, height=40)
        self.itemIcon.grid(row=1, column=0, sticky="nsew")

        self.itemName = tk.Label(self, width=180)
        self.itemName.grid(row=0, column=0, columnspan=2)

        self.itemHave = ttk.Spinbox(self)
        self.itemHave.grid(row=1, column=1)

        # self.itemNeed = ttk.Spinbox(self)
        # self.itemNeed.grid(row=2, column=1)






None
