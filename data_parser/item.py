import collections
import math

from .database import Database


class Item:
    def __init__(self, itemid):
        self.data = Database()
        item = None
        for item in self.data.items["items"].values():
            if item["itemId"] == itemid:
                self.item = item
                break
        self.name = item["name"]
        self.itemId = item["itemId"]
        self.iconId = item["iconId"]
        self.icon = None
        self.rarity = item["rarity"]
        self.formula = []
        if item["buildingProductList"]:
            if item["buildingProductList"][0]["roomType"] == "WORKSHOP":
                self.itemCraftingId = item["buildingProductList"][0]["formulaId"]
                self.formula = self.data.formulas["workshopFormulas"][self.itemCraftingId]
            if item["buildingProductList"][0]["roomType"] == "MANUFACTURE":
                self.itemCraftingId = item["buildingProductList"][0]["formulaId"]
                self.formula = self.data.formulas["manufactFormulas"][self.itemCraftingId]
        self.stages = self.get_stages()
        self.bestAp = math.inf
        self.craftingAp = 0
        self.bestStage = ""
        self.bestStageId = ""
        self.calc_cost()
        self.flags = ""
        self.have = 0

    def get_stages(self):
        results = {}
        results_sorted = collections.OrderedDict()
        for i in range(self.data.materials.__len__()):
            stage = self.data.materials[i].copy()
            if stage["itemId"] == self.itemId:
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
        return results_sorted

    def calc_cost(self):
        if self.stages:
            stage = self.stages.get(next(iter(self.stages)))
            self.bestAp = stage.get("costperitem")
            self.bestStage = self.data.stages[stage["stageId"]]["code"]
            self.bestStageId = stage["stageId"]
        return None
