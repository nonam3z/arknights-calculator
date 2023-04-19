from .database import Database
from .item import Item


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
        try:
            if len(self.ear["phases"]) > 0:
                return self.ear["phases"][int(phase)]["maxLevel"]
            else:
                return 0
        except IndexError:
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
