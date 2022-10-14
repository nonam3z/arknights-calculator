import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import ArknightsDataParser as ADP
import craftingFrame
import farmingFrame
import inventoryFrame as iFrame
import itemDataFrame
import overallPathFrame
import plannerFrame
import stagesFrame


class EarEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ADP.OperatorState):
            return obj.__dict__
        if isinstance(obj, ADP.Stats):
            return obj.__dict__
        if isinstance(obj, ADP.Settings):
            return obj.__dict__
        if isinstance(obj, iFrame.InventoryFrame):
            return obj.__dict__
        if isinstance(obj, ADP.Operator):
            return obj.__dict__
        if isinstance(obj, ADP.Item):
            return obj.__dict__
        if isinstance(obj, ADP.Inventory):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.settings = ADP.Settings()
        self.rep_choose_var = tk.StringVar()
        self.load_settings()
        self.update_variables()

        self.master = master
        self.winfo_toplevel().title("Arknights Calculator")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        master.minsize(width=1300, height=850)
        master.maxsize(width=1300, height=850)
        master.resizable(width=True, height=True)
        self.grid(padx=5, pady=5, sticky="nsew")

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=0, column=0, sticky="nsew")
        self.planner = plannerFrame.Planner(self)
        self.tabs.add(self.planner, text="Planner")
        self.inventory = iFrame.InventoryFrame(self)
        self.tabs.add(self.inventory, text="Inventory Depot")
        self.calculator = overallPathFrame.CalculateFrame(self)
        self.tabs.add(self.calculator, text="Path Calculator")
        self.farming = farmingFrame.FarmingFrame(self)
        self.tabs.add(self.farming, text="Farming Calculator")
        self.crafting = craftingFrame.CraftingFrame(self)
        self.tabs.add(self.crafting, text="Crafting Calculator")
        self.itemData = itemDataFrame.ItemDataFrame(self)
        self.tabs.add(self.itemData, text="Item Data")
        self.stages = stagesFrame.StagesFrame(self)
        self.tabs.add(self.stages, text="Stages List")

        self.menu = tk.Menu(self, tearoff=False)
        self.master.config(menu=self.menu)

        self.settings_menu = tk.Menu(self.menu, tearoff=False)
        self.settings_menu.add_command(label="Clear Inventory", command=self.check_error_typing)
        self.settings_menu.add_command(label="Update Arknights Data",
                                       command=lambda: ADP.update_script(self.rep_choose_var.get(), True))

        self.rep_choose = tk.Menu(self.menu, tearoff=False)
        self.rep_choose.add_checkbutton(label="en-US", onvalue="en_US", variable=self.rep_choose_var,
                                        command=self.change_repository)
        self.rep_choose.add_checkbutton(label="zh-CN", onvalue="zh_CN", variable=self.rep_choose_var,
                                        command=self.change_repository)
        self.rep_choose.add_checkbutton(label="ja-JP", onvalue="ja_JP", variable=self.rep_choose_var,
                                        command=self.change_repository)
        self.rep_choose.add_checkbutton(label="ko-KR", onvalue="ko_KR", variable=self.rep_choose_var,
                                        command=self.change_repository)
        self.rep_choose.add_checkbutton(label="zh-TW", onvalue="zh_TW", variable=self.rep_choose_var,
                                        command=self.change_repository)

        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.menu.add_command(label="About", command=self.about_message)
        self.menu.add_cascade(label="Repository", menu=self.rep_choose)

        self.load_data()

    @staticmethod
    def about_message():
        messagebox.showinfo(title="About", message="Pretty simple Arknights Farming Calculator. \n"
                                                   "Created by nonam3z. \n"
                                                   "Only for educational purposes.")

    def check_error_typing(self):
        checkBox = messagebox.askquestion(title="Clearing Inventory", message="Are you sure? "
                                                                              "This will remove all data from inventory "
                                                                              "tab! \nThis action cannot be undone.")
        if checkBox == "yes":
            self.inventory.clear_inventory()
        return None

    def change_repository(self):
        self.save_data()
        self.update_data()
        self.load_data()

    def update_data(self):
        self.inventory.clear_inventory()
        if os.path.exists("jsons/"+self.rep_choose_var.get()):
            ADP.update_script(self.rep_choose_var.get(), False)
        else:
            ADP.update_script(self.rep_choose_var.get(), True)
        self.update_variables()
        self.planner.selectOperator["values"] = ADP.return_list_of_ears()
        self.inventory.update_inventory()
        self.calculator.create_item_list()
        self.farming.create_item_list()

    def save_data(self):
        earList = self.planner.allEarsList
        data = {"earList": {}, "inventory": {}}
        for ears in earList.values():
            data["earList"][ears.name] = {}
            data["earList"][ears.name]["iid"] = ears.iid
            data["earList"][ears.name]["name"] = ears.name
            data["earList"][ears.name]["current"] = ears.current
            data["earList"][ears.name]["desired"] = ears.desired
        for items in iFrame.InventoryFrame.frames.values():
            data["inventory"][items.itemId] = {}
            data["inventory"][items.itemId]["itemId"] = items.itemId
            if items.itemHave.get():
                data["inventory"][items.itemId]["have"] = items.itemHave.get()
        if os.path.exists("jsons/" + self.settings.repository + "/savedata.json"):
            os.remove("jsons/" + self.settings.repository + "/savedata.json")
        file = open("jsons/" + self.settings.repository + "/savedata.json", 'w+')
        json.dump(data, file, cls=EarEncoder, indent=4)
        file.close()

    @staticmethod
    def save_settings():
        settings_obj = ADP.Settings()
        if os.path.exists("settings.json"):
            os.remove("settings.json")
        file = open("settings.json", 'w+')
        json.dump(settings_obj, file, cls=EarEncoder, indent=4)
        file.close()

    def load_settings(self):
        if os.path.exists("settings.json"):
            size = os.path.getsize("settings.json")
            if size:
                settings = json.load(open("settings.json", encoding='utf-8'))
            else:
                settings = {}
        else:
            settings = {"repository": "en_US"}
        if settings:
            if settings.get("repository"):
                self.settings.repository = settings.get("repository")
                self.rep_choose_var.set(self.settings.repository)
            else:
                self.rep_choose_var.set("en_US")

    def load_data(self):
        if os.path.exists("jsons/" + self.settings.repository + "/savedata.json"):
            size = os.path.getsize("jsons/" + self.settings.repository + "/savedata.json")
            if size:
                self.update_variables()
                savedata = json.load(open("jsons/" + self.settings.repository + "/savedata.json", encoding='utf-8'))
                self.planner.del_all_ears()
                for ear in savedata["earList"].values():
                    name = ear["name"]
                    iid = ear["iid"]
                    sc = ear["current"]
                    sd = ear["desired"]
                    current = ADP.Stats(sc["elite"], sc["level"], sc["skill1"], sc["skill2"],
                                        sc["skill3"])
                    desired = ADP.Stats(sd["elite"], sd["level"], sd["skill1"], sd["skill2"],
                                        sd["skill3"])
                    operator = ADP.OperatorState(iid, name, current, desired)
                    self.planner.allEarsList.setdefault(operator.name)
                    self.planner.allEarsList[operator.name] = operator
                    self.planner.earsList.insert("", tk.END,
                                                 values=(
                                                     name, self.planner.create_upgrade_string(current, desired)),
                                                 iid=iid)
                for item in savedata["inventory"].values():
                    try:
                        iFrame.InventoryFrame.frames[item["itemId"]].itemHave.set(int(item["have"]))
                    except KeyError:
                        pass
        else:
            return None

    def update_variables(self):
        settings_obj = ADP.Settings()
        settings_obj.repository = self.rep_choose_var.get()
        self.save_settings()
        ADP.Database.clear()
        ADP.Database()
        ADP.Inventory.clear()
        ADP.Inventory()
