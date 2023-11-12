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
        self.inventory = { }
        self.data = Database()
        self.inventory = self.create_inventory()
        self.set_item_params()
        if os.path.exists("../jsons/en_US/item_table.json"):
            for item in self.inventory.values():
                self.inventory[item.itemId].name = self.corr_names(item.itemId)

    def create_inventory(self):
        inventory = { }
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

    def set_item_params(self):
        for item in self.inventory:
            self.get_stages(item)
            self.calc_cost(item)
            self.calc_flags(item)
            self.add_some_shitty_formulas(item)
            self.load_icons(item)

    def get_stages(self, item):
        results = { }
        results_sorted = collections.OrderedDict()
        for i in range(self.data.materials.__len__()):
            stage = self.data.materials[i].copy()
            if stage["itemId"] == self.inventory[item].itemId:
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
        self.inventory[item].stages = results_sorted.copy()

    def calc_cost(self, item):
        if self.inventory[item].stages:
            stage = self.inventory[item].stages.get(next(iter(self.inventory[item].stages)))
            self.inventory[item].bestAp = stage.get("costperitem")
            self.inventory[item].bestStage = self.data.stages[stage["stageId"]]["code"]
            self.inventory[item].bestStageId = stage["stageId"]

    def calc_flags(self, item):
        dualchips_id = ["3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283", "32001"]
        if len(self.inventory[item].formula) > 0:
            for i in self.inventory[item].formula["costs"]:
                self.inventory[item].craftingAp += self.inventory[i["id"]].bestAp * i["count"]
        if 0 < self.inventory[item].craftingAp < self.inventory[item].bestAp:
            self.inventory[item].flags = "Crafting"
        else:
            self.inventory[item].flags = "Farming"
        if self.inventory[item].itemId in dualchips_id:
            self.inventory[item].flags = "Crafting"

    def add_some_shitty_formulas(self, item):
        if self.inventory[item].itemId == "4001":
            self.inventory[item].bestAp = 0.004
            self.inventory[item].bestStage = "CE-5"
            self.inventory[item].bestStageId = "wk_melee_5"
            self.inventory[item].stages = {self.inventory[item].bestStageId: self.data.stages[self.inventory[item].bestStageId]}
        elif self.inventory[item].itemId == "5001":
            pass
        elif self.inventory[item].itemId == "32001":
            self.inventory[item].bestAp = 1350
            self.inventory[item].formula = {"costs": []}
            self.inventory[item].formula["costs"].append({"id": "4006", "count": 90, "type": "MATERIAL"})
        elif self.inventory[item].itemId == "4006":
            self.inventory[item].bestAp = 1.5
            self.inventory[item].bestStage = "AP-5"
            self.inventory[item].bestStageId = "wk_toxic_5"
            self.inventory[item].stages = {self.inventory[item].bestStageId: self.data.stages[self.inventory[item].bestStageId]}

    def load_icons(self, item):
        """
        Создает список предметов с иконками для дальнейшей отрисовки таблицы.
        :return: Ничего не возвращает.
        """
        if not os.path.exists(("items/" + self.inventory[item].iconId + ".png")):
            print("Getting image " + self.inventory[item].name + " from github...")
            LoadImages(self.inventory[item].iconId)
        try:
            icon = Image.open("items/" + self.inventory[item].iconId + ".png")
            self.inventory[item].iconSmall, self.inventory[item].iconMedium = icon.copy(), icon.copy()
            self.inventory[item].iconSmall.thumbnail((20, 20), Image.ANTIALIAS)
            self.inventory[item].iconSmall = ImageTk.PhotoImage(self.inventory[item].iconSmall)
            self.inventory[item].iconMedium.thumbnail((36, 36), Image.ANTIALIAS)
            self.inventory[item].iconMedium = ImageTk.PhotoImage(self.inventory[item].iconMedium)
        except FileNotFoundError:
            print("File with id " + self.inventory[item].iconId + " not found, skipping...")
            self.inventory[item].iconSmall = None
            self.inventory[item].iconMedium = None

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
