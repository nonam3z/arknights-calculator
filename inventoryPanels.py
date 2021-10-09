import tkinter as tk
from tkinter import ttk
import json
import ArknightsDataParser as ADP


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

inv = create_inventory()

def calc_cost():
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

calc_cost()




None
