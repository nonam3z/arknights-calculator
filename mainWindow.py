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

savedata = {}

if os.path.exists("savedata.json"):
    size = os.path.getsize("savedata.json")
    if size:
        savedata = json.load(open("savedata.json", encoding='utf-8'))


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.rep_choose_var = tk.StringVar()

        self.master = master
        self.winfo_toplevel().title("Arknights Calculator")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        master.minsize(width=1200, height=900)
        master.maxsize(width=1200, height=900)
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
            self.inventory.clear_inventory()
            ArknightsDataParser.update_script(self.rep_choose_var.get())
            settings = ArknightsDataParser.Settings()
            settings.rep = self.rep_choose_var.get()
            data = ArknightsDataParser.Database()
            data.rep = ArknightsDataParser.Settings().rep
            data.data = ArknightsDataParser.FileRepository(data.rep)
            data.ears = data.data.ears
            data.items = data.data.items
            data.formulas = data.data.formulas
            data.gameconst = data.data.gameconst
            data.materials = data.data.materials
            data.stages = data.data.stages
            self.planner.selectOperator["values"] = ArknightsDataParser.return_list_of_ears()
            self.inventory.update_inventory()
            messagebox.showinfo(title="Complete!", message="Succesful updated all data.")

    def restore_data(self):
        if savedata:
            for ear in savedata["earList"].values():
                name = ear["name"]
                iid = ear["iid"]
                sc = ear["current"]
                sd = ear["desired"]
                current = ArknightsDataParser.Stats(sc["elite"], sc["level"], sc["skill1"], sc["skill2"], sc["skill3"])
                desired = ArknightsDataParser.Stats(sd["elite"], sd["level"], sd["skill1"], sd["skill2"], sd["skill3"])
                operator = ArknightsDataParser.OperatorState(iid, name, current, desired)
                self.planner.allEarsList.setdefault(operator.name)
                self.planner.allEarsList[operator.name] = operator
                self.planner.earsList.insert("", tk.END,
                                             values=(name, self.planner.create_upgrade_string(current, desired)),
                                             iid=iid)
                self.calculator.update()
            for item in savedata["inventory"].values():
                iFrame.InventoryFrame.frames[item["itemId"]].itemHave.set(int(item["have"]))
            if savedata["settings"].get("repository"):
                self.rep_choose_var.set(savedata["settings"]["repository"])
            else:
                self.rep_choose_var.set("en_US")
            self.settings.rep = self.rep_choose_var.get()
