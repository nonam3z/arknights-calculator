from .inventory import Inventory


class PlannerLogic:
    def __init__(self, results=None):

        self.inventory = Inventory().inventory
        self.results_tree = {}
        self.farming_data = {}
        self.crafting_data = {}

    def create_results_tree(self, results=None):
        if results is None:
            results = {}
        results_tree = {}
        for item in results.values():
            if item.formula:
                pass
            else:
                results_tree.setdefault(item.itemId, {"name": item.name, "cost": item.cost, "need": ""})
        return results_tree

    def create_results_tree_branch(self, branch):
        pass



    # def create_results_dict(self, results):
    #     results2 = results.copy()
    #     results = results2.copy()
    #     for item in results:
    #         results[item]["formulas"] = self.create_materials_tree(item, results[item]["need"])
    #     return results
    #
    # def create_materials_tree(self, itemId, need):
    #     chips_id = ["3212", "3222", "3232", "3242", "3252", "3262", "3272", "3282"]
    #     small_chips_id = ["3211", "3221", "3231", "3241", "3251", "3261", "3271", "3281"]
    #     results = {}
    #     if itemId not in chips_id:
    #         if itemId not in small_chips_id:
    #             if DataParser.Inventory().inventory[itemId].formula:
    #                 materials = DataParser.Inventory().inventory[itemId].formula["costs"]
    #                 for m in materials:
    #                     results.setdefault(m["id"], ({"itemId": m["id"], "need": need * m["count"],
    #                                                   "formulas": {}}))
    #                     if DataParser.Inventory().inventory[m["id"]].formula:
    #                         results[m["id"]]["formulas"] = self.create_materials_tree(m["id"], results[m["id"]]["need"])
    #         return results
    #     else:
    #         return results
    #
    # def create_visible_tree(self, results):
    #     self.calculateFrame.delete(*self.calculateFrame.get_children())
    #     self.farming_data = {}
    #     self.crafting_data = {}
    #     inventory = iFrame.InventoryFrame.create_item_list()
    #     results = self.create_results_dict(results)
    #     total_cost = 0
    #     for item in results.values():
    #         self.create_branch(item, "")
    #         if self.inventory[item["itemId"]].flags == "Farming":
    #             if self.farming_data.get(item["itemId"]):
    #                 self.farming_data[item["itemId"]]["need"] = self.farming_data[item["itemId"]] + item["need"]
    #             else:
    #                 self.farming_data.setdefault(item["itemId"], item)
    #     for item in self.calculateFrame.get_children():
    #         if self.calculateFrame.item(item)["values"][2]:
    #             total_cost += int(self.calculateFrame.item(item)["values"][2])
    #     self.master.crafting.create_visible_tree(self.crafting_data)
    #     cdc = self.crafting_data.copy()
    #     self.crafting_data = {}
    #     for item in cdc:
    #         self.crafting_data.setdefault(item, {"itemId": item, "need": int(cdc.get(item)),
    #                                              "formulas": {}})
    #     cdc2 = self.crafting_data.copy()
    #     for item in cdc:
    #         if cdc[item] <= inventory[item]:
    #             cdc2.pop(item)
    #         elif cdc[item] > inventory[item]:
    #             cdc2[item]["need"] = cdc2[item]["need"] - inventory[item]
    #     cdc = cdc2.copy()
    #     self.create_add_farming(self.create_results_dict(cdc))
    #     self.master.farming.create_visible_tree(self.farming_data)
    #     self.text.set("Total item sanity cost: " + str(total_cost))
    #
    # def create_branch(self, item, iid):
    #     stages = DataParser.Database().stages
    #     stage = self.inventory[item["itemId"]].bestStageId
    #     if stage:
    #         runs = math.ceil((self.inventory[item["itemId"]].bestAp * item["need"]) / stages[stage]["apCost"])
    #         cost = runs * stages[stage]["apCost"]
    #     else:
    #         runs = ""
    #         cost = ""
    #     lastIid = self.calculateFrame.insert(iid, tk.END, image=self.inventory[item["itemId"]].icon,
    #                                          values=(
    #                                              self.inventory[item["itemId"]].name, item["need"],
    #                                              cost, runs, self.inventory[item["itemId"]].bestStage
    #                                          ))
    #     if self.inventory[item["itemId"]].flags == "Crafting":
    #         if self.crafting_data.get(item["itemId"]):
    #             self.crafting_data[item["itemId"]] = self.crafting_data[item["itemId"]] + item["need"]
    #         else:
    #             self.crafting_data.setdefault(item["itemId"], item["need"])
    #         if item["formulas"]:
    #             for mat in item["formulas"]:
    #                 self.create_branch(item["formulas"][mat], lastIid)
    #
    # def create_add_farming(self, results):
    #     for item in results:
    #         if results[item]["formulas"]:
    #             for mat in results[item]["formulas"].values():
    #                 self.create_branch_add_farming(mat)
    #     return results
    #
    # def create_branch_add_farming(self, item):
    #     if self.inventory[item["itemId"]].flags == "Farming":
    #         if self.farming_data.get(item["itemId"]):
    #             self.farming_data[item["itemId"]]["need"] = self.farming_data[item["itemId"]]["need"] + item["need"]
    #         else:
    #             self.farming_data.setdefault(item["itemId"], item)
    #     if self.inventory[item["itemId"]].flags == "Crafting":
    #         if self.crafting_data.get(item["itemId"]):
    #             self.crafting_data[item["itemId"]]["need"] = self.crafting_data[item["itemId"]]["need"] + item["need"]
    #         else:
    #             self.crafting_data.setdefault(item["itemId"], item)
    #             if item["formulas"]:
    #                 for mat in item["formulas"]:
    #                     self.create_branch_add_farming(item)
