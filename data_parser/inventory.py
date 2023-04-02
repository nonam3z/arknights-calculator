import json
import os

from .database import Database
from .files_loader import LoadImages
from .item import Item
from .singleton import Singleton


class Inventory(metaclass=Singleton):
    def __init__(self):
        self.inventory = {}
        self.data = Database()
        for item in self.data.items["items"].values():
            if item["itemId"] in ["4001", "5001", "32001", "4006", "mod_unlock_token"]:
                self.inventory[item["itemId"]] = Item(item["itemId"])
            if item["classifyType"] == "MATERIAL" and item["itemType"] == "MATERIAL" and not item["obtainApproach"]:
                self.inventory[item["itemId"]] = Item(item["itemId"])
        self.inventory = self.calc_flags(self.inventory)
        self.inventory = self.add_some_shitty_formulas(self.inventory)
        if os.path.exists("../jsons/en_US/item_table.json"):
            for item in self.inventory.values():
                self.inventory[item.itemId].name = self.corr_names(item.itemId)
        for item in self.inventory.values():
            if not os.path.exists(("items/" + item.iconId + ".png")):
                print("Getting image " + item.name + " from github...")
                LoadImages(item.iconId)

    @staticmethod
    def calc_flags(inv):
        dualchips_id = ["3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283", "32001"]
        for item in inv.values():
            if len(item.formula) > 0:
                for i in item.formula["costs"]:
                    item.craftingAp += inv[i["id"]].bestAp * i["count"]
            if 0 < item.craftingAp < item.bestAp:
                item.flags = "Crafting"
            else:
                item.flags = "Farming"
            if item.itemId in dualchips_id:
                item.flags = "Crafting"
        return inv

    def add_some_shitty_formulas(self, inv):
        for item in inv.values():
            if item.itemId == "4001":
                item.bestAp = 0.004
                item.bestStage = "CE-5"
                item.bestStageId = "wk_melee_5"
                item.stages = self.data.stages.setdefault(item.bestStageId, self.data.stages[item.bestStageId])
            elif item.itemId == "5001":
                pass
            elif item.itemId == "32001":
                item.bestAp = 1350
                item.formula = {"costs": []}
                item.formula["costs"].append({"id": "4006", "count": 90, "type": "MATERIAL"})
            elif item.itemId == "4006":
                item.bestAp = 1.5
                item.bestStage = "AP-5"
                item.bestStageId = "wk_toxic_5"
                item.stages = self.data.stages.setdefault(item.bestStageId, self.data.stages[item.bestStageId])
        return inv

    def corr_names(self, itemid):
        name = ""
        items = json.load(open("../jsons/en_US/item_table.json", encoding='utf-8'))
        for item in items["items"].values():
            if item["itemId"] == itemid:
                name = item["name"]
                break
            else:
                name = self.inventory[itemid].name
        return name

