# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from data_parser import inventory
from data_parser import operator as ADP
from . import planner_modules
from . import planner_panels


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1, minsize=590)
        self.columnconfigure(1, weight=1, minsize=590)
        self.rowconfigure(3, weight=1)

        self.controller = None

        self.selectOperator = ttk.Combobox(self)
        self.selectOperator.insert(0, "Nearl")
        self.selectOperator.grid(row=0, columnspan=2, padx=3, pady=(3, 10), sticky="ew")

        self.stats = tk.Frame(self)
        self.stats.grid(column=0, row=1, padx=0, sticky="nsew")
        self.stats.columnconfigure(0, weight=1)
        self.stats.columnconfigure(1, weight=1)

        self.modules = tk.Frame(self)
        self.modules.grid(column=1, row=1, padx=0, sticky="nsew")
        self.modules.columnconfigure(0, weight=1)
        self.modules.columnconfigure(1, weight=1)

        self.currentStats = planner_panels.StatsPanel(self.stats)
        self.currentStatsView = self.currentStats.view
        self.currentStatsView.grid(column=0, row=0, padx=3, sticky="nsew")

        self.desiredStats = planner_panels.StatsPanel(self.stats)
        self.desiredStatsView = self.desiredStats.view
        self.desiredStatsView.grid(column=1, row=0, padx=3, sticky="nsew")

        self.currentModules = planner_modules.ModulesPanel(self.modules)
        self.currentModules.grid(column=0, row=0, padx=3, sticky="nsew")

        self.desiredModules = planner_modules.ModulesPanel(self.modules)
        self.desiredModules.grid(column=1, row=0, padx=3, sticky="nsew")

        self.leftButtonsFrame = tk.Frame(self)
        self.leftButtonsFrame.grid(column=0, row=2, sticky="ew", pady=(6, 0), padx=(0, 3))
        self.leftButtonsFrame.columnconfigure(0, weight=1)
        self.leftButtonsFrame.columnconfigure(1, weight=1)

        self.buttonAdd = ttk.Button(self.leftButtonsFrame, text="Add Operator")
        self.buttonAdd.grid(column=0, row=0, sticky="ew")
        self.buttonDelete = ttk.Button(self.leftButtonsFrame, text="Delete Operator")
        self.buttonDelete.grid(column=1, row=0, sticky="ew")

        self.rightButtonsFrame = tk.Frame(self)
        self.rightButtonsFrame.grid(column=1, row=2, sticky="ew", pady=(6, 0), padx=(3, 0))
        self.rightButtonsFrame.columnconfigure(0, weight=1)

        self.buttonCalculate = ttk.Button(self.rightButtonsFrame, text="Create Export to Penguin")
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

        self.leftFrame = tk.Frame(self)
        self.leftFrame.grid(column=1, row=3, sticky="nsew", pady=(6, 0), padx=(3, 0))
        self.leftFrame.columnconfigure(0, weight=1)
        self.leftFrame.rowconfigure(0, weight=1)

        self.results = ttk.Treeview(self.leftFrame, columns=["name", "count", "have"])
        self.results.grid(column=0, row=0, sticky="nsew")
        self.results.column("#0", stretch=False, width=75)
        self.results.heading("#0", text="Icon", anchor="center")
        self.results.column("name", stretch=True, width=150)
        self.results.heading("name", text="Item", anchor="center")
        self.results.column("count", stretch=True, width=70)
        self.results.heading("count", text="Need", anchor="center")
        self.results.column("have", stretch=True, width=70)
        self.results.heading("have", text="Have", anchor="center")

    def set_controller(self, controller):
        self.controller = controller


class Model:
    def __init__(self):
        self.ear, self.allEarsList = dict(), dict()

    def get_ears_list(self):
        return ADP.return_list_of_ears()

    def get_item_list(self):
        return inventory.Inventory().inventory

    def get_ear(self, name):
        return ADP.Operator(name)

    def allEarsList_pop(self, name):
        return self.allEarsList.pop(name)

    def allEarsList_get(self, name):
        return self.allEarsList.get(name)

    def allEarsList_replace(self, iid, selectedOp, currStats, desStats):
        op = ADP.OperatorState(iid, selectedOp, currStats, desStats)
        self.allEarsList.setdefault(op.name)
        self.allEarsList[op.name] = op

    def allEarsList_copy(self):
        return self.allEarsList.copy()

    def allEarsList_clear(self):
        self.allEarsList = dict()

    def calculate(self, tpl, earsList):
        """
        Расчет стоимости апгрейда выделенных в списке ушек.
        После расчетов отправляет результат в другие фреймы.
        :return: Возвращает результаты расчетов в виде словарика из "id: count".
        """
        results = {}
        for s in tpl:
            selection = earsList.item(s)
            values = selection.get('values')
            name = values[0]
            for ear in self.allEarsList.values():
                if ear.name == name:
                    self.ear = ear
                    break
            items = self.ear.cost
            if items:
                for i in items.items():
                    count = results.get(i[0], 0)
                    results[i[0]] = count + i[1]
        for item in results:
            results2 = results.copy()
            results[item] = {"itemId": item, "need": int(results2.get(item)),
                             "formulas": {}}
        return results


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.results_list = {}

    def set_binds(self):
        self.view.earsList.bind("<<TreeviewSelect>>", self.create_results_list)
        self.view.selectOperator.bind("<<ComboboxSelected>>", self.set_max_lvls)
        self.view.buttonAdd.configure(command=self.earsList_add)
        self.view.buttonDelete.configure(command=self.earsList_del)

    def load_data(self, earList):
        self.view.selectOperator["values"] = self.model.get_ears_list()
        for ear in earList:
            name = ear["name"]
            iid = ear["iid"]
            sc = ear["current"]
            sd = ear["desired"]
            current = ADP.Stats(sc["elite"], sc["level"], sc["skill1"], sc["skill2"],
                                         sc["skill3"])
            desired = ADP.Stats(sd["elite"], sd["level"], sd["skill1"], sd["skill2"],
                                         sd["skill3"])
            operator = ADP.OperatorState(iid, name, current, desired)
            self.model.allEarsList.setdefault(operator.name)
            self.model.allEarsList[operator.name] = operator
            self.view.earsList.insert("", tk.END, values=(name, self.create_upgrade_string(current, desired)), iid=iid)

    def earsList_add(self):
        """
        По нажатию кнопки Add Operator добавляет ушку в список на прокачку и в словарик объектов с ушками на прокачку.
        """
        allEarsListCopy = self.model.allEarsList_copy()
        selectedOp = self.view.selectOperator.get()
        currStats = self.view.currentStats.controller.construct_op()
        desStats = self.view.desiredStats.controller.construct_op()
        results = self.create_upgrade_string(currStats, desStats)
        if results:
            if allEarsListCopy.get(selectedOp):
                ear = self.model.allEarsList_get(selectedOp)
                self.earsList_del_data(ear.iid, selectedOp)
            iid = self.view.earsList.insert("", tk.END, values=(selectedOp, results))
            self.model.allEarsList_replace(iid, selectedOp, currStats, desStats)

    def earsList_del(self):
        """
        По нажатию кнопки Delete Operator удаляет ушку из таблички ушек и из словарика ушек.
        """
        for i in self.view.results.get_children():
            self.view.results.delete(i)
        for s in self.view.earsList.selection():
            name = self.view.earsList.item(s)
            values = name.get('values')
            self.earsList_del_data(s, values[0])

    def earsList_del_data(self, iid, selectedOp):
        self.view.earsList.delete(iid)
        self.model.allEarsList_pop(selectedOp)

    def get_results(self):
        return self.model.calculate(self.view.earsList.selection(), self.view.earsList)

    def create_results_list(self, event):
        """
        Отображение результатов в фрейме results в виде списка.
        :param event: Принимает на вход event.
        """
        results = self.get_results()
        item_list = self.model.get_item_list()
        for data in results:
            self.results_list[data] = {}
            self.results_list[data]["itemId"] = data
            self.results_list[data]["name"] = item_list[data].name
            self.results_list[data]["iconId"] = item_list[data].iconId
            icon = Image.open("items/" + self.results_list[data]["iconId"] + ".png")
            icon.thumbnail((20, 20), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(icon)
            self.results_list[data]["icon"] = icon
            self.results_list[data]["need"] = results[data]["need"]
            self.results_list[data]["have"] = self.view.master.inventory.view.frames[data].view.itemHave.get()
        for i in self.view.results.get_children():
            self.view.results.delete(i)
        if results:
            for i in results:
                self.view.results.insert("", tk.END, image=self.results_list[i]["icon"],
                                         values=(self.results_list[i]["name"], self.results_list[i]["need"], self.results_list[i]["have"]))
        # self.master.calculator.create_visible_tree(results)

    @staticmethod
    def create_upgrade_string(current, desired):
        """
        Просто создает сокращенную строчку для вывода параметров прокачки в табличку с ушками.
        :param current: Принимает объект с текущими статами ушки.
        :param desired: Принимает объект с желаемыми статами ушки.
        :return: Возвращает сокращенную строчку для вывода в табличку с ушками.
        """
        skills = ["1","2","3","4","5","6","7","M1","M2","M3"]
        results = ""
        if current.elite < desired.elite:
            results = f"{current.elite}e{current.level} to {desired.elite}e{desired.level};  "
        else:
            if current.level < desired.level:
                results = f"{current.elite}e{current.level} to {desired.elite}e{desired.level};  "
        if current.skill1 < desired.skill1 and desired.skill1 > 7:
            results += f"S1({skills[(current.skill1-1)]} to {skills[(desired.skill1-1)]});  "
        if current.skill2 < desired.skill2 and desired.skill2 > 7:
            results += f"S2({skills[(current.skill2-1)]} to {skills[(desired.skill2-1)]});  "
        if current.skill3 < desired.skill3 and desired.skill3 > 7:
            results += f"S3({skills[(current.skill3-1)]} to {skills[(desired.skill3-1)]});  "
        if current.skill1 < desired.skill1 <= 7:
            results += f"SA({skills[(current.skill1-1)]} to {skills[(desired.skill1-1)]});"
        return results

    def set_max_lvls(self, event):
        """
        Выполняет установку ограничений для полей ввода параметров ушки.
        :param event: Принимает на вход event.
        """
        ear = self.model.get_ear(self.view.selectOperator.get())
        self.view.currentStats.controller.set_params(ear.ear["skills"])
        self.view.desiredStats.controller.set_params(ear.ear["skills"])

    def del_all_ears(self):
        self.model.allEarsList_clear()
        self.view.earsList.delete(*self.view.earsList.get_children())


class PlannerFrame:
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.view = View(master=master)
        self.model = Model()
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)

        self.controller.set_binds()
        self.controller.set_max_lvls("")
