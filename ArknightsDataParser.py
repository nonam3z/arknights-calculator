import json


ears = json.load(open("jsons/character_table.json", encoding='utf-8'))
items = json.load(open("jsons/item_table.json", encoding='utf-8'))
formulas = json.load(open("jsons/building_data.json", encoding='utf-8'))
gameconst = json.load(open("jsons/gamedata_const.json", encoding='utf-8'))
# print(ears.values())


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
        self.name = ear["name"]
        self.rarity = ear["rarity"]
        self.maxElite = len(ear["phases"])-1

    def phase(self, phase):
        if len(self.ear["phases"]) > 0:
            return self.ear["phases"][int(phase)]["maxLevel"]
        else:
            return 0

    def skill_lvl(self, phase):
        phase = int(phase)
        if self.rarity > 1:
            if phase == 0:
                return 4
            if phase == 1:
                return 7
            if phase == 2:
                return 10
        else:
            return 1

    def cost(self, elite):
        cost = gameconst["evolveGoldCost"][self.rarity][elite - 1]
        if cost == -1:
            return 0
        else:
            return cost

    def return_elite_cost(self, elite):
        if self.maxElite < elite:
            return []
        else:
            return self.ear["phases"][elite]["evolveCost"]


class Item:
    def __init__(self, itemid):
        item = None
        for item in items["items"].values():
            if item["itemId"] == itemid:
                self.item = item
                break
        self.name = item["name"]
        self.itemId = item["itemId"]
        self.formula = []
        if item["buildingProductList"]:
            if item["buildingProductList"][0]["roomType"] == "WORKSHOP":
                self.itemCraftingId = item["buildingProductList"][0]["formulaId"]
                self.formula = formulas["workshopFormulas"][self.itemCraftingId]


class OperatorState:
    def __init__(self, iid, name, current, desired):
        self.iid = iid
        self.name = name
        self.current = current
        self.desired = desired


class Stats:
    def __init__(self, elite, level, skill1, skill2, skill3):
        self.elite = elite
        self.level = level
        self.skill1 = skill1
        self.skill2 = skill2
        self.skill3 = skill3


def calculate(operator):
    ear = Operator(operator.name)
    results = {}
    max_lvl = []
    need_exp = 0
    need_money = 0
    money_for_elite = 0
    for i in range(0, ear.maxElite+1):
        max_lvl.append(ear.ear["phases"][i]["maxLevel"])
    for elite in range(operator.current.elite, operator.desired.elite+1):
        if elite == operator.current.elite == operator.desired.elite:
            for level in range(operator.current.level-1, operator.desired.level-1):
                need_exp += gameconst["characterExpMap"][elite][level]
                need_money += gameconst["characterUpgradeCostMap"][elite][level]
        if operator.current.elite == elite < operator.desired.elite:
            for level in range(operator.current.level-1, max_lvl[elite]-1):
                need_exp += gameconst["characterExpMap"][elite][level]
                need_money += gameconst["characterUpgradeCostMap"][elite][level]
        if operator.current.elite < elite < operator.desired.elite:
            for level in range(0, max_lvl[elite]-1):
                need_exp += gameconst["characterExpMap"][elite][level]
                need_money += gameconst["characterUpgradeCostMap"][elite][level]
        if operator.current.elite < elite == operator.desired.elite:
            for level in range(0, operator.desired.level-1):
                need_exp += gameconst["characterExpMap"][elite][level]
                need_money += gameconst["characterUpgradeCostMap"][elite][level]
    if need_exp:
        results["EXP"] = need_exp
        results["LMD"] = need_money
    for elite in range(operator.current.elite, operator.desired.elite):
        money_for_elite += gameconst["evolveGoldCost"][ear.rarity][elite]
        for i in return_results(operator.name, elite + 1).items():
            count = results.get(i[0], 0)
            results[i[0]] = count + i[1]
    results["LMD"] = results.get("LMD", 0) + money_for_elite
    if results["LMD"] == 0:
        results.pop("LMD", 0)
    if operator.current.skill1 < operator.desired.skill1 <= 10:
        if operator.desired.skill1 > 7:
            for i in range(operator.current.skill1-1, 6):
                skill_lvl_up_cost = ear.ear["allSkillLvlup"][i]["lvlUpCost"]
                for c in skill_lvl_up_cost:
                    name = Item(c["id"]).name
                    results[name] = results.get(name, 0) + c["count"]
        else:
            for i in range(operator.current.skill1-1, operator.desired.skill1-1):
                skill_lvl_up_cost = ear.ear["allSkillLvlup"][i]["lvlUpCost"]
                for c in skill_lvl_up_cost:
                    name = Item(c["id"]).name
                    results[name] = results.get(name, 0) + c["count"]
    if operator.current.skill1 < operator.desired.skill1 <= 10 and 7 < operator.desired.skill1:
        cost1 = calculate_skills(operator.name, 0, 0, operator.desired.skill1 - 7)
        for i in cost1.items():
            count = results.get(i[0], 0)
            results[i[0]] = count + i[1]
    if operator.current.skill2 < operator.desired.skill2 <= 10 and 7 < operator.desired.skill2:
        cost2 = calculate_skills(operator.name, 1, 0, operator.desired.skill2 - 7)
        for i in cost2.items():
            count = results.get(i[0], 0)
            results[i[0]] = count + i[1]
    if operator.current.skill3 < operator.desired.skill3 <= 10 and 7 < operator.desired.skill3:
        cost3 = calculate_skills(operator.name, 2, 0, operator.desired.skill3 - 7)
        for i in cost3.items():
            count = results.get(i[0], 0)
            results[i[0]] = count + i[1]
    if results != {}:
        return results


def calculate_skills(name, num, current, desired):
    ear = Operator(name)
    lvl_up_cost = ear.ear["skills"][num]["levelUpCostCond"]
    results = {}
    for i in range(current, desired):
        cost = lvl_up_cost[i]["levelUpCost"]
        for c in cost:
            name = Item(c["id"]).name
            results[name] = results.get(name, 0) + c["count"]
    return results


def return_results(name, elite):
    ear = Operator(name)
    if ear.ear is None:
        return {}
    else:
        results = {}
        for item in ear.return_elite_cost(elite):
            i = Item(item["id"])
            results[i.name] = item["count"]
        return results
