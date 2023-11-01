# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import json
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import data_parser as DataParser
from .crafting_frame import CraftingFrame
from .farming_frame import FarmingFrame
from .inventory_frame import InventoryFrame
from .item_data_frame import ItemDataFrame
from .overall_path_frame import OverallPathFrame
from .planner_frame import PlannerFrame
from .stages_frame import StagesFrame


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.controller = None
        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.rep_choose_var = tk.StringVar(value="en_US")

        self.winfo_toplevel().title("Arknights Calculator")

        master.minsize(width=1300, height=850)
        master.geometry("1300x850")
        master.resizable(width=True, height=True)

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=0, column=0, sticky="nsew")
        self.planner = PlannerFrame(self)
        self.tabs.add(self.planner.view, text="Planner")
        self.inventory = InventoryFrame(self)
        self.tabs.add(self.inventory.view, text="Inventory Depot")
        self.calculator = OverallPathFrame(self)
        self.tabs.add(self.calculator, text="Path Calculator")
        self.farming = FarmingFrame(self)
        self.tabs.add(self.farming.view, text="Farming Calculator")
        self.crafting = CraftingFrame(self)
        self.tabs.add(self.crafting.view, text="Crafting Calculator")
        self.itemData = ItemDataFrame(self)
        self.tabs.add(self.itemData, text="Item Data")
        self.stages = StagesFrame(self)
        self.tabs.add(self.stages.view, text="Stages List")

        self.menu = tk.Menu(self, tearoff=False)
        self.master.config(menu=self.menu)

        self.settings_menu = tk.Menu(self.menu, tearoff=False)
        self.settings_menu.add_command(label="Clear Inventory")
        self.settings_menu.add_command(label="Update Arknights Data")

        self.rep_choose = tk.Menu(self.menu, tearoff=False)
        self.rep_choose.add_checkbutton(label="en-US", onvalue="en_US", variable=self.rep_choose_var)
        self.rep_choose.add_checkbutton(label="ja-JP", onvalue="ja_JP", variable=self.rep_choose_var)
        self.rep_choose.add_checkbutton(label="ko-KR", onvalue="ko_KR", variable=self.rep_choose_var)

        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.menu.add_command(label="About")
        self.menu.add_cascade(label="Repository", menu=self.rep_choose)

    def set_controller(self, controller):
        self.controller = controller


class Model:
    def __init__(self):
        pass

    class EarEncoder(json.JSONEncoder):
        """
        JSONEncoder for all classes in calc. \n
        Allows save of data in readable json.dict.
        """
        def default(self, obj):
            """
            Default method for JSONEncoder. \n
            :param obj: class
            :return: serializable json.dict
            """
            instances = (
                DataParser.operator.OperatorState,
                DataParser.operator.Stats,
                DataParser.operator.Operator,
                DataParser.settings.Settings,
                DataParser.inventory.Item,
                DataParser.inventory.Inventory
            )
            if isinstance(obj, instances):
                return obj.__dict__
            return json.JSONEncoder.default(self, obj)

    def save_data(self, controller, earlist, rep, stages, inventory, settings):
        data = {"earList": {}, "inventory": {}, "stages": {}}
        for ears in earlist.values():
            data["earList"][ears.name] = {}
            data["earList"][ears.name]["iid"] = ears.iid
            data["earList"][ears.name]["name"] = ears.name
            data["earList"][ears.name]["current"] = ears.current
            data["earList"][ears.name]["desired"] = ears.desired
        for items in inventory:
            data["inventory"][items] = {}
            data["inventory"][items]["itemId"] = items
            if inventory[items]:
                data["inventory"][items]["have"] = inventory[items]
            else:
                data["inventory"][items]["have"] = 0
        data["stages"].setdefault("checked_list", stages)
        if os.path.exists(f"jsons/{rep}/savedata.json"):
            os.remove(f"jsons/{rep}/savedata.json")
        file = open(f"jsons/{rep}/savedata.json", 'w+')
        json.dump(data, file, cls=self.EarEncoder, indent=4)
        file.close()
    pass

    def load_data(self):
        repository = DataParser.settings.Settings().repository
        if os.path.exists(f"jsons/{repository}/savedata.json"):
            size = os.path.getsize(f"jsons/{repository}/savedata.json")
            if size:
                savedata = json.load(open(f"jsons/{repository}/savedata.json", encoding='utf-8'))
                return savedata
            else:
                return None
        else:
            return None


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        pass

    def set_binds(self):
        self.view.tabs.bind("<<NotebookTabChanged>>", self.update_tabs_data)
        self.view.settings_menu.entryconfigure("Clear Inventory", command=self.check_error_typing)
        self.view.settings_menu.entryconfigure("Update Arknights Data",
                                       command=lambda: DataParser.files_loader.FileRepository(self.view.rep_choose_var.get(), True))
        self.view.menu.entryconfigure("About", command=self.about_message)
        for i in range(0, self.view.rep_choose.index(tk.END)):
            self.view.rep_choose.entryconfigure(i, command=self.change_repository)

    def change_repository(self):
        if self.view.rep_choose_var.get() in ["en_US", "ja_JP", "ko_KR"]:
            self.save_data()
            self.update_data()
            self.view.calculator.clear_all()
            self.view.farming.controller.clear_all()
            self.view.crafting.controller.clear_all()
            self.view.itemData.clear_all()
            self.model.load_data()
            self.view.itemData.create_info()
        else:
            self.view.rep_choose_var.set(DataParser.settings.Settings().repository)

    def update_data(self):
        self.view.inventory.clear_inventory()
        if os.path.exists("jsons/" + self.view.rep_choose_var.get()):
            DataParser.files_loader.FileRepository(self.view.rep_choose_var.get(), False)
        else:
            DataParser.files_loader.FileRepository(self.view.rep_choose_var.get(), True)
        self.update_variables()
        self.view.planner.view.selectOperator["values"] = DataParser.operator.return_list_of_ears()
        self.view.inventory.update_inventory()
        self.view.calculator.model.create_item_list()
        self.view.farming.model.create_item_list()
        DataParser.settings.Settings().repository = self.view.rep_choose_var.get()

    def save_data(self):
        try:
            self.model.save_data(self, self.view.planner.model.allEarsList, self.view.rep_choose_var.get(),
                                 self.view.stages.controller.get_checked_stages(),
                                 self.view.inventory.controller.create_current_stash_list(), dict())
        except ValueError:
            pass

    def load_data(self):
        try:
            savedata = self.model.load_data()
            self.update_variables()
            self.view.planner.controller.del_all_ears()
            if savedata["earList"]:
                try:
                    self.view.planner.controller.load_data(savedata["earList"].values())
                except KeyError:
                    print("KeyError in savedata.json --> earList.")
            if savedata["inventory"]:
                try:
                    for item in savedata["inventory"].values():
                        self.view.inventory.view.frames[item["itemId"]].view.itemHave.set(int(item["have"]))
                except KeyError:
                    print("KeyError in savedata.json --> inventory.")
            if savedata["stages"]:
                try:
                    self.view.stages.controller.clear_all()
                    self.view.stages.controller.create_stages_tree(checked_list=savedata["stages"]["checked_list"])
                except KeyError:
                    self.view.stages.controller.clear_all()
                    self.view.stages.controller.create_stages_tree()
                    print("KeyError in savedata.json --> stages.")
        except ValueError:
            pass

    def update_variables(self):
        settings_obj = DataParser.settings.Settings()
        settings_obj.repository = self.view.rep_choose_var.get()
        # self.save_settings()
        DataParser.database.Database.clear()
        DataParser.database.Database()
        DataParser.inventory.Inventory.clear()
        DataParser.inventory.Inventory()

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
            self.view.inventory.clear_inventory()
        return None

    def update_tabs_data(self, event):
        pass
        # self.view.planner.create_results_list("")
        # self.update()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

        self.view = View(master=self)
        self.model = Model()
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)

        self.protocol("WM_DELETE_WINDOW", self.save_data)

        self.controller.set_binds()
        self.load_data()

    def save_data(self):
        self.controller.save_data()
        # self.controller.save_settings()
        self.destroy()

    def load_data(self):
        self.controller.load_data()

    def start_program(self):
        self.mainloop()





