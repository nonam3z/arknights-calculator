import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import ArknightsDataParser
import calculateFrame
import farmingFrame
import inventoryFrame as iFrame
import plannerFrame


class EarEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ArknightsDataParser.OperatorState):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Stats):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Settings):
            return obj.__dict__
        if isinstance(obj, iFrame.InventoryFrame):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Operator):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Item):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Inventory):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.rep_choose_var = tk.StringVar()

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
        self.calculator = calculateFrame.CalculateFrame(self)
        self.tabs.add(self.calculator, text="Path Calculator")
        self.farming = farmingFrame.FarmingFrame(self)
        self.tabs.add(self.farming, text="Farming Calculator")
        self.settings = ArknightsDataParser.Settings()

        self.menu = tk.Menu(self, tearoff=False)
        self.master.config(menu=self.menu)

        self.settings_menu = tk.Menu(self.menu, tearoff=False)
        self.settings_menu.add_command(label="Clear Inventory", command=self.check_error_typing)
        self.settings_menu.add_command(label="Update Arknights Data", command=self.update_data)

        self.rep_choose = tk.Menu(self.menu, tearoff=False)
        self.rep_choose.add_checkbutton(label="en-US", onvalue="en_US", variable=self.rep_choose_var,
                                        command=self.update_data)
        self.rep_choose.add_checkbutton(label="zh-CN", onvalue="zh_CN", variable=self.rep_choose_var,
                                        command=self.update_data)
        self.rep_choose.add_checkbutton(label="ja-JP", onvalue="ja_JP", variable=self.rep_choose_var,
                                        command=self.update_data)
        self.rep_choose.add_checkbutton(label="ko-KR", onvalue="ko_KR", variable=self.rep_choose_var,
                                        command=self.update_data)
        self.rep_choose.add_checkbutton(label="zh-TW", onvalue="zh_TW", variable=self.rep_choose_var,
                                        command=self.update_data)
        self.rep_choose_var.set("en_US")

        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.menu.add_command(label="About", command=self.about_message)
        self.menu.add_cascade(label="Repository", menu=self.rep_choose)

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

    def update_data(self):
        checkBox = messagebox.askquestion(title="Changing Repository", message="Are you sure? \n"
                                                                               "This potentially can corrupt data "
                                                                               "stored in ears list.\nProceed with caution!")
        if checkBox == "yes":
            self.save_data()
            self.inventory.clear_inventory()
            ArknightsDataParser.update_script(self.rep_choose_var.get())
            settings_obj = ArknightsDataParser.Settings()
            settings_obj.repository = self.rep_choose_var.get()
            self.save_settings()
            data = ArknightsDataParser.Database()
            data.rep = ArknightsDataParser.Settings().repository
            data.data = ArknightsDataParser.FileRepository(data.rep)
            data.ears = data.data.ears
            data.items = data.data.items
            data.formulas = data.data.formulas
            data.gameconst = data.data.gameconst
            data.materials = data.data.materials
            data.stages = data.data.stages
            self.planner.selectOperator["values"] = ArknightsDataParser.return_list_of_ears()
            self.inventory.update_inventory()
            self.restore_data()
            messagebox.showinfo(title="Complete!", message="Succesful updated all data.")

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

    def save_settings(self):
        settings_obj = ArknightsDataParser.Settings()
        if os.path.exists("settings.json"):
            os.remove("settings.json")
        file = open("settings.json", 'w+')
        json.dump(settings_obj, file, cls=EarEncoder, indent=4)
        file.close()

    def restore_data(self):
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
            if os.path.exists("jsons/" + self.settings.repository + "/savedata.json"):
                size = os.path.getsize("jsons/" + self.settings.repository + "/savedata.json")
                if size:
                    savedata = json.load(open("jsons/" + self.settings.repository + "/savedata.json", encoding='utf-8'))
                    self.planner.del_all_ears()
                    for ear in savedata["earList"].values():
                        name = ear["name"]
                        iid = ear["iid"]
                        sc = ear["current"]
                        sd = ear["desired"]
                        current = ArknightsDataParser.Stats(sc["elite"], sc["level"], sc["skill1"], sc["skill2"],
                                                            sc["skill3"])
                        desired = ArknightsDataParser.Stats(sd["elite"], sd["level"], sd["skill1"], sd["skill2"],
                                                            sd["skill3"])
                        operator = ArknightsDataParser.OperatorState(iid, name, current, desired)
                        self.planner.allEarsList.setdefault(operator.name)
                        self.planner.allEarsList[operator.name] = operator
                        self.planner.earsList.insert("", tk.END,
                                                     values=(
                                                         name, self.planner.create_upgrade_string(current, desired)),
                                                     iid=iid)
                        self.calculator.update()
                    for item in savedata["inventory"].values():
                        iFrame.InventoryFrame.frames[item["itemId"]].itemHave.set(int(item["have"]))
            else:
                return None
