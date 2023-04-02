# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import ttk

from data_parser import operator
from . import planner_modules
from . import planner_stats


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

        self.currentStats = planner_stats.StatsPanel(self.stats)
        self.currentStatsView = self.currentStats.view
        self.currentStatsView.grid(column=0, row=0, padx=3, sticky="nsew")

        self.desiredStats = planner_stats.StatsPanel(self.stats)
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
        self.ear = 0
        self.allEarsList = {}
        self.list = {}
        self.path = {}
        self.item_list = {}

    def get_ears_list(self):
        return operator.return_list_of_ears()


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def set_binds(self):
        # self.view.earsList.bind("<<TreeviewSelect>>", self.create_results_list)
        # self.view.selectOperator.bind("<<ComboboxSelected>>", self.set_max_lvls)
        self.view.buttonAdd.bind(self.add_ear_to_list)

    def load_data(self):
        self.view.selectOperator["values"] = self.model.get_ears_list()

    def add_ear_to_list(self):
        """
        По нажатию кнопки Add Operator добавляет ушку в список на прокачку и в словарик объектов с ушками на прокачку.
        """
        earlist = self.model.allEarsList.copy()
        name = self.view.selectOperator.get()
        currStats = self.view.currentStats.controller.construct_op()
        desStats = self.view.desiredStats.construct_op()
        results = self.create_upgrade_string(currStats, desStats)
        selectedOp = self.view.selectOperator.get()
        if results:
            if earlist.get(name):
                ear = self.model.allEarsList.get(name)
                self.model.earsList.delete(ear.iid)
                self.model.allEarsList.pop(name)
                iid = self.model.earsList.insert("", tk.END, values=(selectedOp, results))
                op = operator.OperatorState(iid, selectedOp, currStats, desStats)
                self.model.allEarsList.setdefault(op.name)
                self.model.allEarsList[op.name] = op
            else:
                iid = self.model.earsList.insert("", tk.END, values=(selectedOp, results))
                op = operator.OperatorState(iid, selectedOp, currStats, desStats)
                self.model.allEarsList.setdefault(op.name)
                self.model.allEarsList[op.name] = op

    @staticmethod
    def create_upgrade_string(current, desired):
        """
        Просто создает сокращенную строчку для вывода параметров прокачки в табличку с ушками.
        :param current: Принимает объект с текущими статами ушки.
        :param desired: Принимает объект с желаемыми статами ушки.
        :return: Возвращает сокращенную строчку для вывода в табличку с ушками.
        """
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


class PlannerFrame:
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.view = View(master=master)
        self.model = Model()
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)

        self.controller.load_data()
        self.controller.set_binds()

        # def calculate(self):
        #     """
        #     Расчет стоимости апгрейда выделенных в списке ушек.
        #     После расчетов отправляет результат в другие фреймы.
        #     :return: Возвращает результаты расчетов в виде словарика из "id: count".
        #     """
        #     results = {}
        #     tpl = self.earsList.selection()
        #     for s in tpl:
        #         selection = self.earsList.item(s)
        #         values = selection.get('values')
        #         name = values[0]
        #         for ear in self.allEarsList.values():
        #             if ear.name == name:
        #                 self.ear = ear
        #                 break
        #         items = self.ear.cost
        #         if items:
        #             for i in items.items():
        #                 count = results.get(i[0], 0)
        #                 results[i[0]] = count + i[1]
        #     for item in results:
        #         results2 = results.copy()
        #         item_data = ADP.Inventory().inventory[item]
        #         results[item] = {"itemId": item, "need": int(results2.get(item)),
        #                          "formulas": {}}
        #     return results
        #
        # # noinspection PyUnusedLocal
        # def create_results_list(self, event):
        #     """
        #     Отображение результатов в фрейме results в виде списка.
        #     :param event: Принимает на вход event.
        #     """
        #     results = self.calculate()
        #     self.item_list = ADP.Inventory().inventory
        #     for data in results:
        #         self.list[data] = {}
        #         self.list[data]["itemId"] = data
        #         self.list[data]["name"] = self.item_list[data].name
        #         self.list[data]["iconId"] = self.item_list[data].iconId
        #         icon = Image.open("items/" + self.list[data]["iconId"] + ".png")
        #         icon.thumbnail((20, 20), Image.ANTIALIAS)
        #         icon = ImageTk.PhotoImage(icon)
        #         self.list[data]["icon"] = icon
        #         self.list[data]["need"] = results[data]["need"]
        #         self.list[data]["have"] = iFrame.InventoryFrame.frames[data].itemHave.get()
        #     for i in self.results.get_children():
        #         self.results.delete(i)
        #     if results:
        #         for i in results:
        #             self.results.insert("", tk.END, image=self.list[i]["icon"],
        #                                 values=(self.list[i]["name"], self.list[i]["need"], self.list[i]["have"]))
        #     self.master.calculator.create_visible_tree(results)
        #
        #
        # @staticmethod
        # def create_upgrade_string(current, desired):
        #     """
        #     Просто создает сокращенную строчку для вывода параметров прокачки в табличку с ушками.
        #     :param current: Принимает объект с текущими статами ушки.
        #     :param desired: Принимает объект с желаемыми статами ушки.
        #     :return: Возвращает сокращенную строчку для вывода в табличку с ушками.
        #     """
        #     results = ""
        #     if int(current.elite) < int(desired.elite):
        #         results += (str(current.elite) + "e" + str(current.level) + " >>> "
        #                     + str(desired.elite) + "e" + str(desired.level) + "; ")
        #     if (int(current.elite) == int(desired.elite)) and (
        #             int(current.level) < int(desired.level)):
        #         results += (str(current.elite) + "e" + str(current.level) + " >>> "
        #                     + str(desired.elite) + "e" + str(desired.level) + "; ")
        #     if int(current.skill1) < int(desired.skill1):
        #         results += ("S1(" + str(current.skill1) + " to " + str(desired.skill1) + "); ")
        #     if int(current.skill2) < int(desired.skill2):
        #         results += ("S2(" + str(current.skill2) + " to " + str(desired.skill2) + "); ")
        #     if int(current.skill3) < int(desired.skill3):
        #         results += ("S3(" + str(current.skill3) + " to " + str(desired.skill3) + "); ")
        #     return results
        #
        # def del_ear_from_list(self):
        #     """
        #     По нажатию кнопки Delete Operator удаляет ушку из таблички ушек и из словарика ушек.
        #     """
        #     for i in self.results.get_children():
        #         self.results.delete(i)
        #     for s in self.earsList.selection():
        #         name = self.earsList.item(s)
        #         values = name.get('values')
        #         self.earsList.delete(s)
        #         self.allEarsList.pop(values[0])
        #     # self.create_path_list()
        #
        # def del_all_ears(self):
        #     for ear in self.earsList.get_children():
        #         self.earsList.delete(ear)
        #     self.allEarsList = {}
        #
        # # noinspection PyUnusedLocal
        # def set_max_lvls(self, event):
        #     """
        #     Выполняет установку ограничений для полей ввода параметров ушки.
        #     :param event: Принимает на вход event.
        #     """
        #     ear = ADP.Operator(self.selectOperator.get())
        #     self.currentStats.clear_spinboxes()
        #     self.desiredStats.clear_spinboxes()
        #     self.currentStats.callback("<Current stats update.>")
        #     self.desiredStats.callback("<Desired stats update.>")
        #     self.skills_counter(ear.ear["skills"])
        #
        # def skills_counter(self, skills):
        #     """
        #     Управляет работой полей ввода, отключая ненужные в зависимости от редкости ушки.
        #     :param skills: Принимает на вход массив skills ушки, рассчитывая на его основе количество навыков ушки.
        #     """
        #     self.currentStats.selectSkill1.configure(state=DISABLED)
        #     self.currentStats.selectSkill2.configure(state=DISABLED)
        #     self.currentStats.selectSkill3.configure(state=DISABLED)
        #     self.desiredStats.selectSkill1.configure(state=DISABLED)
        #     self.desiredStats.selectSkill2.configure(state=DISABLED)
        #     self.desiredStats.selectSkill3.configure(state=DISABLED)
        #     if len(skills) >= 1:
        #         self.currentStats.selectSkill1.configure(state=NORMAL)
        #         self.desiredStats.selectSkill1.configure(state=NORMAL)
        #     if len(skills) >= 2:
        #         self.currentStats.selectSkill2.configure(state=NORMAL)
        #         self.desiredStats.selectSkill2.configure(state=NORMAL)
        #     if len(skills) == 3:
        #         self.currentStats.selectSkill3.configure(state=NORMAL)
        #         self.desiredStats.selectSkill3.configure(state=NORMAL)
