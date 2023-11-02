import collections
import json
import math
import os

from PIL import Image, ImageTk

from .database import Database
from .files_loader import LoadImages
from .item import Item
from .singleton import Singleton


class Inventory(metaclass=Singleton):
    def __init__(self):
        self.inventory = {}
        self.data = Database()
        self.inventory = self.create_inventory()
        self.get_stages()
        self.calc_flags()
        self.add_some_shitty_formulas()
        if os.path.exists("../jsons/en_US/item_table.json"):
            for item in self.inventory.values():
                self.inventory[item.itemId].name = self.corr_names(item.itemId)
        for item in self.inventory.values():
            if not os.path.exists(("items/" + item.iconId + ".png")):
                print("Getting image " + item.name + " from github...")
                LoadImages(item.iconId)
        self.load_icons()

    def create_inventory(self):
        inventory = {}
        for item in self.data.items["items"].values():
            if item["itemId"] in ["4001", "5001", "32001", "4006", "mod_unlock_token"]:
                inventory[item["itemId"]] = Item(item["itemId"], item["name"], item["iconId"], item["rarity"])
            if item["classifyType"] == "MATERIAL" and item["itemType"] == "MATERIAL" and not item["obtainApproach"]:
                inventory[item["itemId"]] = Item(item["itemId"], item["name"], item["iconId"], item["rarity"])
        for item in inventory.values():
            if self.data.items["items"][item.itemId]["buildingProductList"]:
                if self.data.items["items"][item.itemId]["buildingProductList"][0]["roomType"] == "WORKSHOP":
                    item.itemCraftingId = self.data.items["items"][item.itemId]["buildingProductList"][0]["formulaId"]
                    item.formula = self.data.formulas["workshopFormulas"][item.itemCraftingId]
                if self.data.items["items"][item.itemId]["buildingProductList"][0]["roomType"] == "MANUFACTURE":
                    item.itemCraftingId = self.data.items["items"][item.itemId]["buildingProductList"][0]["formulaId"]
                    item.formula = self.data.formulas["manufactFormulas"][item.itemCraftingId]
        return inventory

    def get_stages(self):
        results = {}
        results_sorted = collections.OrderedDict()
        for item in self.inventory.values():
            for i in range(self.data.materials.__len__()):
                stage = self.data.materials[i].copy()
                if stage["itemId"] == item.itemId:
                    results[stage["stageId"]] = stage
                    if stage.get("stageId") in Database().stages:
                        results[stage["stageId"]].setdefault("name", self.data.stages[stage["stageId"]]["code"])
                    if self.data.stages.get(stage["stageId"]):
                        results[stage["stageId"]].setdefault("stagecost", self.data.stages[stage["stageId"]]["apCost"])
                    else:
                        results[stage["stageId"]].setdefault("stagecost", math.inf)
                    results[stage["stageId"]].setdefault("percentage", (stage["quantity"] / stage["times"]))
                    if stage.get("percentage") > 0:
                        results[stage["stageId"]].setdefault("costperitem", (stage.get("stagecost") / stage.get("percentage")))
                    else:
                        results[stage["stageId"]].setdefault("costperitem", math.inf)
            for k, v in sorted(results.items(), key=lambda x: x[1]["costperitem"]):
                results_sorted.setdefault(k, v)
            for stage in results_sorted:
                results_sorted[stage] = results[stage]
            item.stages = results_sorted.copy()

    def calc_cost(self):
        for item in self.inventory.values():
            if item.stages:
                stage = item.stages.get(next(iter(item.stages)))
                item.bestAp = stage.get("costperitem")
                item.bestStage = self.data.stages[stage["stageId"]]["code"]
                item.bestStageId = stage["stageId"]
            return None

    def calc_flags(self):
        dualchips_id = ["3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283", "32001"]
        for item in self.inventory.values():
            if len(item.formula) > 0:
                for i in item.formula["costs"]:
                    item.craftingAp += self.inventory[i["id"]].bestAp * i["count"]
            if 0 < item.craftingAp < item.bestAp:
                item.flags = "Crafting"
            else:
                item.flags = "Farming"
            if item.itemId in dualchips_id:
                item.flags = "Crafting"

    def add_some_shitty_formulas(self):
        for item in self.inventory.values():
            if item.itemId == "4001":
                item.bestAp = 0.004
                item.bestStage = "CE-5"
                item.bestStageId = "wk_melee_5"
                item.stages = {item.bestStageId: self.data.stages[item.bestStageId]}
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
                item.stages = {item.bestStageId: self.data.stages[item.bestStageId]}

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

    def load_icons(self):
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

