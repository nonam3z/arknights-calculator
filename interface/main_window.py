# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import json
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

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

        self.rep_choose_var = tk.StringVar()

        self.winfo_toplevel().title("Arknights Calculator")

        master.minsize(width=1300, height=850)
        master.geometry("1300x850")
        master.resizable(width=True, height=True)

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=0, column=0, sticky="nsew")
        self.planner = PlannerFrame(self)
        self.tabs.add(self.planner.view, text="Planner")
        self.inventory = InventoryFrame(self)
        self.tabs.add(self.inventory, text="Inventory Depot")
        self.calculator = OverallPathFrame(self)
        self.tabs.add(self.calculator, text="Path Calculator")
        self.farming = FarmingFrame(self)
        self.tabs.add(self.farming, text="Farming Calculator")
        self.crafting = CraftingFrame(self)
        self.tabs.add(self.crafting, text="Crafting Calculator")
        self.itemData = ItemDataFrame(self)
        self.tabs.add(self.itemData, text="Item Data")
        self.stages = StagesFrame(self)
        self.tabs.add(self.stages, text="Stages List")

        self.menu = tk.Menu(self, tearoff=False)
        self.master.config(menu=self.menu)

        self.settings_menu = tk.Menu(self.menu, tearoff=False)
        self.settings_menu.add_command(label="Clear Inventory")
        self.settings_menu.add_command(label="Update Arknights Data")

        self.rep_choose = tk.Menu(self.menu, tearoff=False)
        self.rep_choose.add_checkbutton(label="en-US", onvalue="en_US", variable=self.rep_choose_var)
        self.rep_choose.add_checkbutton(label="zh-CN", onvalue="zh_CN", variable=self.rep_choose_var)
        self.rep_choose.add_checkbutton(label="ja-JP", onvalue="ja_JP", variable=self.rep_choose_var)
        self.rep_choose.add_checkbutton(label="ko-KR", onvalue="ko_KR", variable=self.rep_choose_var)
        self.rep_choose.add_checkbutton(label="zh-TW", onvalue="zh_TW", variable=self.rep_choose_var)

        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.menu.add_command(label="About")
        self.menu.add_cascade(label="Repository", menu=self.rep_choose)

    def set_controller(self, controller):
        self.controller = controller


class Model:
    def __init__(self):
        pass

    class EarEncoder(json.JSONEncoder):
        def default(self, obj):
            instances = (
                ADP.OperatorState,
                ADP.Stats,
                ADP.Settings,
                iFrame.InventoryFrame,
                ADP.Operator,
                ADP.Item,
                ADP.Inventory
            )
            if isinstance(obj, instances):
                return obj.__dict__
            return json.JSONEncoder.default(self, obj)

    def save_data(self, earlist, rep, stages, inventory, settings):
        data = {"earList": {}, "inventory": {}, "stages": {}}
        for ears in earlist.values():
            data["earList"][ears.name] = {}
            data["earList"][ears.name]["iid"] = ears.iid
            data["earList"][ears.name]["name"] = ears.name
            data["earList"][ears.name]["current"] = ears.current
            data["earList"][ears.name]["desired"] = ears.desired
        for items in InventoryFrame.frames.values():
            data["inventory"][items.itemId] = {}
            data["inventory"][items.itemId]["itemId"] = items.itemId
            if items.itemHave.get():
                data["inventory"][items.itemId]["have"] = items.itemHave.get()
        data["stages"].setdefault("checked_list", stages)
        if os.path.exists("jsons/" + rep + "/savedata.json"):
            os.remove("jsons/" + rep + "/savedata.json")
        file = open("jsons/" + rep + "/savedata.json", 'w+')
        json.dump(data, file, cls=EarEncoder, indent=4)
        file.close()
    pass

    def load_data(self):
        pass


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        pass

    def save_data(self):
        try:
            self.model.save_data(self, )
        except ValueError:
            pass

    def load_data(self):
        try:
            self.model.load_data(self)
        except ValueError:
            pass

    @staticmethod
    def about_message():
        messagebox.showinfo(title="About", message="Pretty simple Arknights Farming Calculator. \n"
                                                   "Created by nonam3z. \n"
                                                   "Only for educational purposes.")


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

    def save_data(self):
        # self.app.save_data()
        # self.app.save_settings()
        self.destroy()

    def start_program(self):
        self.mainloop()



        # self.tabs.bind("<<NotebookTabChanged>>", self.update_tabs_data)
        # self.settings_menu.add_command(label="Clear Inventory", command=self.check_error_typing)
        # self.settings_menu.add_command(label="Update Arknights Data",
        #                                command=lambda: ADP.LoadFiles(self.rep_choose_var.get(), True).run())

