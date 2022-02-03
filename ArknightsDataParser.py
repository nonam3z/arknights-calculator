import json
import math
import urllib.request
from urllib.request import urlretrieve
from urllib.request import getproxies
import os

import requests

os.makedirs("jsons", exist_ok=True)


def get_file_from_github(filename):
    repository = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/"
    data = (repository + filename + ".json")
    file = ("jsons/" + filename + ".json")
    os.remove(file)
    open(file, 'w+')
    urlretrieve(data, file)


def get_penguin_data():
    repository = "https://penguin-stats.io/PenguinStats/api/v2/result/matrix.json?show_closed_zones=false&server=US"
    file = "jsons/materials.json"
    os.remove(file)
    open(file, 'w+')
    urlretrieve(repository, file)


def update_script():
    session = requests.session()
    session.proxies = getproxies()
    print("Getting characters data...")
    get_file_from_github("character_table")
    print("Getting items data...")
    get_file_from_github("item_table")
    print("Getting formulas data...")
    get_file_from_github("building_data")
    print("Getting game constants...")
    get_file_from_github("gamedata_const")
    print("Getting stages data...")
    get_file_from_github("stage_table")
    print("Download complete!")
    # get_penguin_data()


# update_script()


ears = json.load(open("jsons/character_table.json", encoding='utf-8'))
items = json.load(open("jsons/item_table.json", encoding='utf-8'))
formulas = json.load(open("jsons/building_data.json", encoding='utf-8'))
gameconst = json.load(open("jsons/gamedata_const.json", encoding='utf-8'))
materials = json.load(open("jsons/materials.json", encoding='utf-8'))
stages = json.load(open("jsons/stage_table.json", encoding='utf-8'))
materials = materials["matrix"]
stages = stages["stages"]


def return_list_of_ears():
    earlist = []
    for ear in ears.values():
        if ear["displayNumber"]:
            earlist.append(ear["name"])
    earlist.sort()
    return earlist


class Operator:
    def __init__(self, name):
        ear = None
        for ear in ears.values():
            if ear["name"] == name:
                self.ear = ear
                break

    def phase(self, phase):
        if len(self.ear["phases"]) > 0:
            return self.ear["phases"][int(phase)]["maxLevel"]
        else:
            return 0

    def skill_lvl(self, phase):
        phase = int(phase)
        if self.ear["rarity"] > 1:
            if phase == 0:
                return 4
            if phase == 1:
                return 7
            if phase == 2:
                return 10
        else:
            return 1

    def cost(self, elite):
        cost = gameconst["evolveGoldCost"][self.ear["rarity"]][elite - 1]
        if cost == -1:
            return 0
        else:
            return cost

    def elite_cost(self, elite):
        if (len(self.ear["phases"]) - 1) < elite:
            return []
        else:
            return self.ear["phases"][elite]["evolveCost"]


class Inventory:
    def __init__(self):
        self.items = {}
        for item in items["items"].values():
            if item["itemId"] == "4001" or item["itemId"] == "5001":
                self.items[item["itemId"]] = Item(item["itemId"])
            if item["classifyType"] == "MATERIAL" and item["itemType"] == "MATERIAL" and not item["obtainApproach"]:
                self.items[item["itemId"]] = Item(item["itemId"])


class Item:
    def __init__(self, itemid):
        item = None
        for item in items["items"].values():
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
                self.formula = formulas["workshopFormulas"][self.itemCraftingId]
        self.stages = self.get_stages()
        self.bestAp = math.inf
        self.craftingAp = 0
        self.bestStage = ""
        self.bestStageId = ""
        self.calc_cost()
        self.flags = ""
        self.need = 0
        self.have = 0

    def get_stages(self):
        results = {}
        for i in range(materials.__len__()):
            stage = materials[i]
            if stage["itemId"] == self.itemId:
                results[stage["stageId"]] = stage
        return results

    def calc_cost(self):
        for stage in self.stages.values():
            if stages.get(stage["stageId"]):
                ap_cost = stages[stage["stageId"]]["apCost"]
            else:
                ap_cost = math.inf
            percentage = stage["quantity"] / stage["times"]
            if percentage > 0:
                best_ap = ap_cost / percentage
            else:
                best_ap = math.inf
            if best_ap < self.bestAp:
                self.bestAp = math.trunc(best_ap)
                self.bestStage = stages[stage["stageId"]]["code"]
                self.bestStageId = stage["stageId"]
        return None


def create_inventory():
    inv = Inventory()
    return inv


def calc_flags():
    for item in inventory.items.values():
        if len(item.formula) > 0:
            for i in item.formula["costs"]:
                item.craftingAp += inventory.items[i["id"]].bestAp * i["count"]
        if 0 < item.craftingAp < item.bestAp:
            item.flags = "Crafting"
        else:
            item.flags = "Farming"
    return None


inventory = create_inventory()
calc_flags()


class OperatorState:
    def __init__(self, iid, name, current, desired):
        self.iid = iid
        self.name = name
        self.operator = Operator(self.name)
        self.current = current
        self.desired = desired
        self.cost = {}
        self.calc_cost()

    def calc_cost(self):
        max_lvl = []
        for i in range(0, len(self.operator.ear["phases"])):
            max_lvl.append(self.operator.ear["phases"][i]["maxLevel"])
        for elite in range(self.current.elite, self.desired.elite + 1):
            if elite == self.current.elite == self.desired.elite:
                self.calc_needs(self.current.level - 1, self.desired.level - 1, elite)
            if self.current.elite == elite < self.desired.elite:
                self.calc_needs(self.current.level - 1, max_lvl[elite] - 1, elite)
            if self.current.elite < elite < self.desired.elite:
                self.calc_needs(0, max_lvl[elite] - 1, elite)
            if self.current.elite < elite == self.desired.elite:
                self.calc_needs(0, self.desired.level - 1, elite)
        for elite in range(self.current.elite, self.desired.elite):
            self.cost["4001"] = self.cost.get("4001", 0) + gameconst["evolveGoldCost"][self.operator.ear["rarity"]][
                elite]
            for i in self.return_results(elite + 1).items():
                count = self.cost.get(i[0], 0)
                self.cost[i[0]] = count + i[1]
        if self.current.skill1 < self.desired.skill1:
            if self.desired.skill1 > 7:
                desired = 6
            else:
                desired = self.desired.skill1 - 1
            for i in range(self.current.skill1 - 1, desired):
                skill_lvl_up_cost = self.operator.ear["allSkillLvlup"][i]["lvlUpCost"]
                for c in skill_lvl_up_cost:
                    name = Item(c["id"]).itemId
                    self.cost[name] = self.cost.get(name, 0) + c["count"]
        if self.current.skill1 < self.desired.skill1 <= 10 and 7 < self.desired.skill1:
            cost1 = self.calculate_skills(0, self.current.skill1 - 7, self.desired.skill1 - 7)
            for i in cost1.items():
                count = self.cost.get(i[0], 0)
                self.cost[i[0]] = count + i[1]
        if self.current.skill2 < self.desired.skill2 <= 10 and 7 < self.desired.skill2:
            cost2 = self.calculate_skills(1, self.current.skill2 - 7, self.desired.skill2 - 7)
            for i in cost2.items():
                count = self.cost.get(i[0], 0)
                self.cost[i[0]] = count + i[1]
        if self.current.skill3 < self.desired.skill3 <= 10 and 7 < self.desired.skill3:
            cost3 = self.calculate_skills(2, self.current.skill3 - 7, self.desired.skill3 - 7)
            for i in cost3.items():
                count = self.cost.get(i[0], 0)
                self.cost[i[0]] = count + i[1]
        return None

    def calc_needs(self, lvlmin, lvlmax, elite):
        for level in range(lvlmin, lvlmax):
            self.cost["5001"] = self.cost.get("5001", 0) + gameconst["characterExpMap"][elite][level]
            self.cost["4001"] = self.cost.get("4001", 0) + gameconst["characterUpgradeCostMap"][elite][level]
        return None

    def return_results(self, elite):
        results = {}
        for item in self.operator.elite_cost(elite):
            i = Item(item["id"])
            results[i.itemId] = item["count"]
        return results

    def calculate_skills(self, num, current, desired):
        lvl_up_cost = self.operator.ear["skills"][num]["levelUpCostCond"]
        results = {}
        if current < 0:
            current = 0
        for i in range(current, desired):
            cost = lvl_up_cost[i]["levelUpCost"]
            for c in cost:
                name = Item(c["id"]).itemId
                results[name] = results.get(name, 0) + c["count"]
        return results


class Stats:
    def __init__(self, elite, level, skill1, skill2, skill3):
        self.elite = elite
        self.level = level
        self.skill1 = skill1
        self.skill2 = skill2
        self.skill3 = skill3
