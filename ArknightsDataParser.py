# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import collections
import datetime
import json
import math
import os
import threading

import github
import requests


def get_images_from_github(filename):
    repository = "https://raw.githubusercontent.com/Aceship/Arknight-Images/main/items/"
    url = (repository + filename + ".png")
    os.makedirs("items/", exist_ok=True)
    file = ("items/" + filename + ".png")
    if os.path.exists(file):
        if os.path.getsize(file) == 0:
            os.remove(file)
    if not os.path.exists(file):
        data = requests.get(url=url).content
        if data.__len__() > 20:
            open(file, 'wb+').write(data)


class LoadFiles(threading.Thread):
    def __init__(self, rep, force):
        super().__init__()

        self.rep, self.force = rep, force

    def run(self):
        """
        Создание/обновление базы данных для работы программы.
        """
        date_github = self.check_github()
        if os.path.exists("jsons/" + self.rep):
            date_file = datetime.datetime.fromtimestamp(os.path.getmtime(("jsons/" + self.rep)))
        else:
            date_file = datetime.datetime.now()
        print(str(date_github) + " // git -- file // " + str(date_file) + " // rep: " + self.rep)
        bool_check = date_github > date_file
        print("Check git > file: " + str(bool_check))
        if (date_github > date_file) or (self.force is True):
            os.makedirs("jsons", exist_ok=True)
            print("Getting characters data...")
            self.get_file("character_table")
            print("Getting items data...")
            self.get_file("item_table")
            print("Getting formulas data...")
            self.get_file("building_data")
            print("Getting game constants...")
            self.get_file("gamedata_const")
            print("Getting module data...")
            self.get_file("uniequip_table")
            print("Getting zones data...")
            self.get_file("zone_table")
            print("Getting stages data...")
            self.get_file("stage_table")
        print("Getting matrix data...")
        self.get_penguin_matrix()
        print("Update complete!")

    def check_github(self):
        try:
            g = github.Github()
            repo = g.get_repo("Aceship/AN-EN-Tags")
            commits = repo.get_commits(path=("json/gamedata/" + self.rep + "/gamedata"))
            date = commits[0].commit.committer.date
        except github.GithubException:
            date = datetime.datetime.fromtimestamp(0)
        return date

    def get_file(self, filename):
        """
        Метод для получения файлов из репозитория github.
        :param filename: Принимает на вход имя файла.
        """
        repository = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/" + str(
            self.rep) + "/gamedata/excel/"
        url = (repository + filename + ".json")
        os.makedirs(("jsons/" + self.rep + "/"), exist_ok=True)
        file = ("jsons/" + self.rep + "/" + filename + ".json")
        if os.path.exists(file):
            os.remove(file)
        data = requests.get(url=url).json()
        open(file, 'w+').write(json.dumps(data))

    def get_penguin_matrix(self):
        """
        Метод для получения матрицы стоимости и частоты выпадения материалов с Penguin Statistics.
        """
        repository = "https://penguin-stats.io/PenguinStats/api/v2/result/matrix"
        file = "jsons/" + self.rep + "/materials.json"
        reps = ["en_US", "zh_CN", "ja_JP", "ko_KR", "zh_TW"]
        servers = ["US", "CN", "JP", "KR", "CN"]
        if self.rep in reps:
            server = servers[reps.index(self.rep)]
        else:
            server = "US"
        if os.path.exists(file):
            os.remove(file)
        PARAMS = {"server": server, "show_closed_zones": False}
        data = str(requests.get(url=repository, params=PARAMS).content)
        data = data[2:-1:]
        open(file, 'w+').write(data)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls):
        cls._instances = {}


class FileRepository:
    def __init__(self, rep):
        self.ears = {}
        self.items = {}
        self.formulas = {}
        self.gameconst = {}
        self.materials = {}
        self.stages = {}
        self.zones = {}
        self.modules = {}
        try:
            self.load_files(rep)
        except json.JSONDecodeError as error:
            for file_name in os.listdir("jsons/" + rep):
                if os.path.isfile("jsons/" + rep + "/" + file_name):
                    os.remove("jsons/" + rep + "/" + file_name)
            LoadFiles(rep, True).run()
            self.load_files(rep)
        except FileNotFoundError as error:
            print("Database is corrupted or missing, redownloading...")
            LoadFiles(rep, True).run()
            self.load_files(rep)

    def load_files(self, rep):
        self.ears = json.load(open("jsons/" + rep + "/character_table.json", encoding='utf-8'))
        self.items = json.load(open("jsons/" + rep + "/item_table.json", encoding='utf-8'))
        self.formulas = json.load(open("jsons/" + rep + "/building_data.json", encoding='utf-8'))
        self.gameconst = json.load(open("jsons/" + rep + "/gamedata_const.json", encoding='utf-8'))
        self.materials = json.load(open("jsons/" + rep + "/materials.json", encoding='utf-8'))["matrix"]
        self.stages = json.load(open("jsons/" + rep + "/stage_table.json", encoding='utf-8'))["stages"]
        self.zones = json.load(open("jsons/" + rep + "/zone_table.json", encoding='utf-8'))["zones"]
        self.modules = json.load(open("jsons/" + rep + "/uniequip_table.json", encoding='utf-8'))


class Savedata:
    def __init__(self):
        self.savedata = json.load(open("savedata.json", encoding='utf-8'))


class Settings(metaclass=Singleton):
    def __init__(self):
        self.repository = "en_US"


class Database(metaclass=Singleton):
    def __init__(self):
        self.rep = Settings().repository
        self.data = FileRepository(self.rep)
        self.ears = self.data.ears
        self.items = self.data.items
        self.formulas = self.data.formulas
        self.gameconst = self.data.gameconst
        self.materials = self.data.materials
        self.stages = self.data.stages
        self.zones = self.data.zones
        self.modules = self.data.modules


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
        if os.path.exists("jsons/en_US/item_table.json"):
            for item in self.inventory.values():
                self.inventory[item.itemId].name = self.corr_names(item.itemId)
        for item in self.inventory.values():
            if not os.path.exists(("items/" + item.iconId + ".png")):
                print("Getting image " + item.name + " from github...")
                get_images_from_github(item.iconId)

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
        items = json.load(open("jsons/en_US/item_table.json", encoding='utf-8'))
        for item in items["items"].values():
            if item["itemId"] == itemid:
                name = item["name"]
                break
            else:
                name = self.inventory[itemid].name
        return name


def return_list_of_ears():
    """
    Создание списка ушек для работы основного фрейма.
    :return: Возращает список имен ушек в виде массива.
    """
    earlist = []
    data = Database()
    if data.rep == "en_US":
        for ear in data.ears.values():
            if ear["displayNumber"]:
                earlist.append(ear["name"])
    else:
        for ear in data.ears.values():
            if ear["displayNumber"]:
                earlist.append(ear["appellation"])
    earlist.sort()
    return earlist


class Operator:
    def __init__(self, name):
        self.data = Database()
        for ear in self.data.ears.values():
            if self.data.rep == "en_US":
                if ear["name"] == name:
                    self.ear = ear
                    break
            else:
                if ear["appellation"] == name:
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
        cost = self.data.gameconst["evolveGoldCost"][self.ear["rarity"]][elite - 1]
        if cost == -1:
            return 0
        else:
            return cost

    def elite_cost(self, elite):
        if (len(self.ear["phases"]) - 1) < elite:
            return []
        else:
            return self.ear["phases"][elite]["evolveCost"]


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


class OperatorState:
    def __init__(self, iid, name, current, desired):
        self.data = Database()
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
            self.cost["4001"] = self.cost.get("4001", 0) + \
                                self.data.gameconst["evolveGoldCost"][self.operator.ear["rarity"]][elite]
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
            self.cost["5001"] = self.cost.get("5001", 0) + self.data.gameconst["characterExpMap"][elite][level]
            self.cost["4001"] = self.cost.get("4001", 0) + self.data.gameconst["characterUpgradeCostMap"][elite][level]
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
