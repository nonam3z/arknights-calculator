import tkinter as tk
from tkinter import ttk
from tkinter import *

import inventoryFrame
import plannerPanels
import ArknightsDataParser
import win32clipboard
import json
import math
from PIL import Image, ImageTk


class Planner(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        self.master = master
        self.ear = 0
        self.allEarsList = {}
        self.list = {}

        self.style = ttk.Style()

        self.selectOperator = ttk.Combobox(self)
        self.selectOperator.insert(0, "Nearl")
        self.selectOperator["values"] = ArknightsDataParser.return_list_of_ears()
        self.selectOperator.grid(row=0, columnspan=2, padx=3, pady=(3, 10), sticky="ew")
        self.selectOperator.bind("<<ComboboxSelected>>", self.set_max_lvls)

        self.currentStats = plannerPanels.CalcPanel(self)
        self.currentStats.grid(column=0, row=1, padx=3, sticky="nsew")

        self.desiredStats = plannerPanels.CalcPanel(self)
        self.desiredStats.grid(column=1, row=1, padx=3, sticky="nsew")

        self.leftButtonsFrame = tk.Frame(self)
        self.leftButtonsFrame.grid(column=0, row=2, sticky="ew", pady=(6, 0), padx=(0, 3))
        self.leftButtonsFrame.columnconfigure(0, weight=1)
        self.leftButtonsFrame.columnconfigure(1, weight=1)

        self.buttonAdd = tk.Button(self.leftButtonsFrame, text="Add Operator", command=self.add_ear_to_list)
        self.buttonAdd.grid(column=0, row=0, sticky="ew")
        self.buttonDelete = tk.Button(self.leftButtonsFrame, text="Delete Operator", command=self.del_ear_from_list)
        self.buttonDelete.grid(column=1, row=0, sticky="ew")

        self.rightButtonsFrame = tk.Frame(self)
        self.rightButtonsFrame.grid(column=1, row=2, sticky="ew", pady=(6, 0), padx=(3, 0))
        self.rightButtonsFrame.columnconfigure(0, weight=1)

        self.buttonCalculate = tk.Button(self.rightButtonsFrame, text="Calculate", command=self.calculate_button)
        self.buttonCalculate.grid(column=0, row=0, sticky="ew")

        self.rightFrame = tk.Frame(self)
        self.rightFrame.grid(column=0, row=3, sticky="nsew", pady=(6, 0), padx=(0, 3))
        self.rightFrame.columnconfigure(0, weight=1)
        self.rightFrame.rowconfigure(0, weight=1)

        self.earsList = ttk.Treeview(self.rightFrame, show="headings", columns=["name", "desired"],
                                     selectmode=tk.EXTENDED)
        self.earsList.grid(column=0, row=0, sticky="nsew")
        self.earsList.column("name", stretch=False, width=150)
        self.earsList.heading("name", text="Name", anchor="center")
        self.earsList.column("desired", stretch=True, width=100)
        self.earsList.heading("desired", text="Desired changes", anchor="center")
        self.earsList.bind("<<TreeviewSelect>>", self.create_results_list)

        self.leftFrame = tk.Frame(self)
        self.leftFrame.grid(column=1, row=3, sticky="nsew", pady=(6, 0), padx=(3, 0))
        self.leftFrame.columnconfigure(0, weight=1)
        self.leftFrame.rowconfigure(0, weight=1)

        # self.results = ttk.Listbox(self.leftFrame, relief="sunken", bg="#FFFFFF", justify="left", activestyle='none',
        #                           takefocus=0, selectmode=tk.EXTENDED)
        self.results = ttk.Treeview(self.leftFrame, columns=["name", "count", "have"])
        self.results.grid(column=0, row=0, sticky="nsew")
        self.results.column("#0", stretch=False, width=75)
        self.results.heading("#0", text="Icon", anchor="center")
        self.results.column("name", stretch=True, width=100)
        self.results.heading("name", text="Item", anchor="center")
        self.results.column("count", stretch=True, width=100)
        self.results.heading("count", text="Count", anchor="center")
        self.results.column("have", stretch=True, width=100)
        self.results.heading("have", text="Have", anchor="center")
        # self.style.configure("Treeview", rowheight=50)
        # self.results["width"] = self.leftFrame.winfo_width()
        # self.results["height"] = self.leftFrame.winfo_height()

        self.set_max_lvls("")

    def calculate_button(self):
        results = self.calculate("")
        penguin_export = {}
        json_data = {"@type":"@penguin-statistics/planner/config"}
        items_dict = {}
        options = {"options":{"byProduct":"false", "requireExp":"true", "requireLmb":"true"}}
        excludes = ["main_06-14","main_07-01","main_07-02","main_07-03","main_07-04","main_07-05",
                                  "main_07-06","main_07-07","main_07-08","main_07-09","main_07-10","main_07-11",
                                  "main_07-12","main_07-13","main_07-14","main_07-15","main_07-16","sub_07-1-1",
                                  "sub_07-1-2","main_08-01","main_08-02","main_08-03","main_08-04","main_08-05",
                                  "main_08-06","main_08-07","main_08-08","main_08-09","main_08-10","main_08-11",
                                  "main_08-12","main_08-13","main_08-14","main_08-15","main_08-16","main_08-17"]
        excludes_dict = {}
        items = []
        for i in results:
            items.append({'id': i, 'need': results.get(i, 0), 'have':0})
        items_dict.setdefault("items", items)
        excludes_dict.setdefault("excludes", excludes)
        penguin_export.update(json_data)
        penguin_export.update(items_dict)
        penguin_export.update(options)
        penguin_export.update(excludes_dict)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(json.dumps(penguin_export))
        win32clipboard.CloseClipboard()

    def calculate(self): # Расчет стоимости апгрейда выделенных в списке ушек.
        results = {}
        tpl = self.earsList.selection()
        for s in tpl:
            selection = self.earsList.item(s)
            values = selection.get('values')
            name = values[0]
            for ear in self.allEarsList.values():
                if ear.name == name:
                    self.ear = ear
                    break
            items = ArknightsDataParser.calculate(self.ear)
            if items:
                for i in items.items():
                    count = results.get(i[0], 0)
                    results[i[0]] = count + i[1]
        return results

    def create_results_list(self, event):  # Отображение списка результатов.
        results = self.calculate()
        for l in results:
            self.list[l] = {}
            self.list[l]["itemId"] = l
            self.list[l]["name"] = ArknightsDataParser.Item(l).name
            self.list[l]["iconId"] = ArknightsDataParser.Item(l).iconId
            icon = Image.open("items/" + self.list[l]["iconId"] + ".png")
            icon.thumbnail((20, 20), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(icon)
            self.list[l]["icon"] = icon
            self.list[l]["need"] = results.get(l)
            self.list[l]["have"] = inventoryFrame.frames[l].itemHave.get()
        for i in self.results.get_children():
            self.results.delete(i)
        if results:
            for i in results:
                self.results.insert("", tk.END, image=self.list[i]["icon"],
                                    values=(self.list[i]["name"], self.list[i]["need"], self.list[i]["have"]))

    def add_ear_to_list(self):
        earlist_copy = self.allEarsList.copy()
        name = self.selectOperator.get()
        results = self.create_upgrade_string(self.currentStats.construct_op(), self.desiredStats.construct_op())
        if results:
            if earlist_copy.get(name):
                ear = self.allEarsList.get(name)
                self.earsList.delete(ear.iid)
                self.allEarsList.pop(name)
                iid = self.earsList.insert("", tk.END, values=(self.selectOperator.get(), results))
                operator = ArknightsDataParser.OperatorState(iid, self.selectOperator.get(),
                                                             self.currentStats.construct_op(),
                                                             self.desiredStats.construct_op())
                self.allEarsList.setdefault(operator.name)
                self.allEarsList[operator.name] = operator
            else:
                iid = self.earsList.insert("", tk.END, values=(self.selectOperator.get(), results))
                operator = ArknightsDataParser.OperatorState(iid, self.selectOperator.get(),
                                                             self.currentStats.construct_op(),
                                                             self.desiredStats.construct_op())
                self.allEarsList.setdefault(operator.name)
                self.allEarsList[operator.name] = operator

    def create_upgrade_string(self, current, desired):
        results = ""
        if int(current.elite) < int(desired.elite):
            results += (str(current.elite) + "e" + str(current.level) + " >>> "
                        + str(desired.elite) + "e" + str(desired.level) + "; ")
        if (int(current.elite) == int(desired.elite)) and (
                int(current.level) < int(desired.level)):
            results += (str(current.elite) + "e" + str(current.level) + " >>> "
                        + str(desired.elite) + "e" + str(desired.level) + "; ")
        if int(current.skill1) < int(desired.skill1):
            results += ("S1(" + str(current.skill1) + " to " + str(desired.skill1) + "); ")
        if int(current.skill2) < int(desired.skill2):
            results += ("S2(" + str(current.skill2) + " to " + str(desired.skill2) + "); ")
        if int(current.skill3) < int(desired.skill3):
            results += ("S3(" + str(current.skill3) + " to " + str(desired.skill3) + "); ")
        return results

        # e1 = str(operator.current.elite)
        # e2 = str(operator.desired.elite)
        # lvl1 = str(operator.current.level)
        # lvl2 = str(operator.desired.level)
        # self.earsList.insert(tk.END, str(operator.name + ": " + e1 + "e" + lvl1 + " >> " + e2 + "e" + lvl2))

    def del_ear_from_list(self):
        for i in self.results.get_children():
            self.results.delete(i)
        for s in self.earsList.selection():
            name = self.earsList.item(s)
            values = name.get('values')
            self.earsList.delete(s)
            self.allEarsList.pop(values[0])

    def set_max_lvls(self, event):
        ear = ArknightsDataParser.Operator(self.selectOperator.get())
        self.currentStats.clear_spinboxes()
        self.desiredStats.clear_spinboxes()
        self.currentStats.callback()
        self.desiredStats.callback()
        self.skills_counter(ear.skills)

    def skills_counter(self, skills):
        self.currentStats.selectSkill1.configure(state=DISABLED)
        self.currentStats.selectSkill2.configure(state=DISABLED)
        self.currentStats.selectSkill3.configure(state=DISABLED)
        self.desiredStats.selectSkill1.configure(state=DISABLED)
        self.desiredStats.selectSkill2.configure(state=DISABLED)
        self.desiredStats.selectSkill3.configure(state=DISABLED)
        if len(skills) >= 1:
            self.currentStats.selectSkill1.configure(state=NORMAL)
            self.desiredStats.selectSkill1.configure(state=NORMAL)
        if len(skills) >= 2:
            self.currentStats.selectSkill2.configure(state=NORMAL)
            self.desiredStats.selectSkill2.configure(state=NORMAL)
        if len(skills) == 3:
            self.currentStats.selectSkill3.configure(state=NORMAL)
            self.desiredStats.selectSkill3.configure(state=NORMAL)

