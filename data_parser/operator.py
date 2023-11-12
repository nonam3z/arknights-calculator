from .database import Database
from .inventory import Inventory


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
        if self.ear["rarity"] != "TIER_1":
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
        self.iid = iid
        self.name = name
        self.current = current
        self.desired = desired
        self.cost = OperatorCost(iid, name, current, desired).get_cost()


# noinspection PyMethodMayBeStatic
class OperatorCost:
    def __init__(self, iid, name, current, desired):
        self.operator = Operator(name)
        self.inventory = Inventory().inventory
        self.gameconst = Database().gameconst
        self.cost = self.calc_cost(current, desired)

    def get_cost(self):
        return self.cost

    def calc_cost(self, current, desired):
        current_skills = [current.skill1, current.skill2, current.skill3]
        desired_skills = [desired.skill1, desired.skill2, desired.skill3]
        elite_cost = self.get_elite_cost(current.elite, desired.elite, current.level, desired.level, self.get_maxlvls())
        elite_items = self.get_elite_items(current.elite, desired.elite)
        skills_lvlup_items = self.get_skills_lvlup_items(current_skills, desired_skills)
        skills_mastery_items = self.get_skills_mastery_items(current_skills, desired_skills)
        combined_cost = self.combine_cost([elite_cost, elite_items, skills_lvlup_items, skills_mastery_items])
        return combined_cost

    def combine_cost(self, cost):
        combined_cost = {}
        for part in cost:
            for item in part:
                if item not in combined_cost.keys():
                    combined_cost.setdefault(item, part.get(item))
                else:
                    combined_cost[item] = combined_cost.get(item) + part.get(item)
        return combined_cost

    def get_maxlvls(self):
        max_lvls = []
        for i in range(0, len(self.operator.ear["phases"])):
            max_lvls.append(self.operator.ear["phases"][i]["maxLevel"])
        return max_lvls

    def get_elite_cost(self, curr_elite, des_elite, curr_level, des_level, max_lvls):
        elite_cost = {}
        for elite in range(curr_elite, des_elite + 1):
            if elite == curr_elite == des_elite:
                elite_cost = self.calc_money_exp(curr_level - 1, des_level - 1, elite, elite_cost)
            if curr_elite == elite < des_elite:
                elite_cost = self.calc_money_exp(curr_level - 1, max_lvls[elite] - 1, elite, elite_cost)
            if curr_elite < elite < des_elite:
                elite_cost = self.calc_money_exp(0, max_lvls[elite] - 1, elite, elite_cost)
            if curr_elite < elite == des_elite:
                elite_cost = self.calc_money_exp(0, des_level - 1, elite, elite_cost)
        return elite_cost

    def calc_money_exp(self, lvlmin, lvlmax, elite, cost):
        for level in range(lvlmin, lvlmax):
            cost["5001"] = cost.get("5001", 0) + self.gameconst["characterExpMap"][elite][level]
            cost["4001"] = cost.get("4001", 0) + self.gameconst["characterUpgradeCostMap"][elite][level]
        return cost

    def get_elite_items(self, curr_elite, des_elite):
        cost = {}
        for elite in range(curr_elite, des_elite):
            cost["4001"] = cost.get("4001", 0) + \
                           self.gameconst["evolveGoldCost"][(int(self.operator.ear["rarity"][5])-1)][elite]
            for i in self.return_elite_items(elite + 1).items():
                count = cost.get(i[0], 0)
                cost[i[0]] = count + i[1]
        return cost

    def get_skills_lvlup_items(self, current, desired):
        cost = {}
        if current[0] < desired[0]:
            for i in range(current[0] - 1, min(max(desired[0] - 1, 0), 6)):
                skill_lvl_up_cost = self.operator.ear["allSkillLvlup"][i]["lvlUpCost"]
                for c in skill_lvl_up_cost:
                    name = self.inventory[c["id"]].itemId
                    cost[name] = cost.get(name, 0) + c["count"]
        return cost

    def get_skills_mastery_items(self, current, desired):
        cost = {}
        for i in range(2):
            if current[i] < desired[i] <= 10 and 7 < desired[i]:
                cost = self.return_skills_mastery_cost(0, current[i] - 7, desired[i] - 7)
                for n in cost.items():
                    count = cost.get(n[0], 0)
                    cost[n[0]] = count + n[1]
        return cost

    def return_elite_items(self, elite):
        results = {}
        for item in self.operator.elite_cost(elite):
            i = self.inventory[item["id"]]
            results[i.itemId] = item["count"]
        return results

    def return_skills_mastery_cost(self, num, current, desired):
        lvl_up_cost = self.operator.ear["skills"][num]["levelUpCostCond"]
        results = {}
        if current < 0:
            current = 0
        for i in range(current, desired):
            cost = lvl_up_cost[i]["levelUpCost"]
            for c in cost:
                name = self.inventory[c["id"]].itemId
                results[name] = results.get(name, 0) + c["count"]
        return results

    def create_cost_tree(self, cost):
        results = {}
        for itemId in cost:
            item = self.inventory[itemId]
            results.setdefault(itemId, item)
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
