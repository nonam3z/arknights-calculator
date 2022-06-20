import json
import tkinter as tk
from tkinter import *
from tkinter import ttk

import win32clipboard
from PIL import Image, ImageTk

import ArknightsDataParser as ADP
import inventoryFrame as iFrame
import plannerPanels


class Planner(tk.Frame):
    results = {}

    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1, minsize=590)
        self.columnconfigure(1, weight=1, minsize=590)
        self.rowconfigure(3, weight=1)

        self.master = master
        self.ear = 0
        self.allEarsList = {}
        self.list = {}
        self.path = {}
        self.item_list = {}

        self.style = ttk.Style()

        self.selectOperator = ttk.Combobox(self)
        self.selectOperator.insert(0, "Nearl")
        self.selectOperator["values"] = ADP.return_list_of_ears()
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

        self.buttonCalculate = tk.Button(self.rightButtonsFrame, text="Create Export to Penguin",
                                         command=self.calculate_button)
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
        self.results.column("name", stretch=True, width=150)
        self.results.heading("name", text="Item", anchor="center")
        self.results.column("count", stretch=True, width=70)
        self.results.heading("count", text="Need", anchor="center")
        self.results.column("have", stretch=True, width=70)
        self.results.heading("have", text="Have", anchor="center")
        # self.style.configure("Treeview", rowheight=50)
        # self.results["width"] = self.leftFrame.winfo_width()
        # self.results["height"] = self.leftFrame.winfo_height()

        self.set_max_lvls("")

    def calculate_button(self):
        """
        Собирает результаты расчетов для поушкивания и упаковывает их в словарик.
        Добавляет в словарик ограничения по зонам, а так же параметры конфигурации для PStats.
        Словарик в дальнейшем копируется для использования в Penguin Statistics (импорт значений для фарма).
        """
        results = self.calculate()
        penguin_export = {}
        json_data = {"@type": "@penguin-statistics/planner/config"}
        items_dict = {}
        options = {"options": {"byProduct": "false", "requireExp": "true", "requireLmb": "true"}}
        excludes = ["main_06-14", "main_07-01", "main_07-02", "main_07-03", "main_07-04", "main_07-05",
                    "main_07-06", "main_07-07", "main_07-08", "main_07-09", "main_07-10", "main_07-11",
                    "main_07-12", "main_07-13", "main_07-14", "main_07-15", "main_07-16", "sub_07-1-1",
                    "sub_07-1-2", "main_08-01", "main_08-02", "main_08-03", "main_08-04", "main_08-05",
                    "main_08-06", "main_08-07", "main_08-08", "main_08-09", "main_08-10", "main_08-11",
                    "main_08-12", "main_08-13", "main_08-14", "main_08-15", "main_08-16", "main_08-17"]
        excludes_dict = {}
        items = []
        for i in results:
            items.append({'id': i, 'need': results.get(i, 0), 'have': iFrame.InventoryFrame.frames[i].itemHave.get()})
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

    def calculate(self):
        """
        Расчет стоимости апгрейда выделенных в списке ушек.
        После расчетов отправляет результат в другие фреймы.
        :return: Возвращает результаты расчетов в виде словарика из "id: count".
        """
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
            items = self.ear.cost
            if items:
                for i in items.items():
                    count = results.get(i[0], 0)
                    results[i[0]] = count + i[1]
        self.master.calculator.create_path(results)
        return results

    # noinspection PyUnusedLocal
    def create_results_list(self, event):
        """
        Отображение результатов в фрейме results в виде списка.
        :param event: Принимает на вход event.
        """
        results = self.calculate()
        self.item_list = ADP.Inventory().inventory
        for data in results:
            self.list[data] = {}
            self.list[data]["itemId"] = data
            self.list[data]["name"] = self.item_list[data].name
            self.list[data]["iconId"] = self.item_list[data].iconId
            icon = Image.open("items/" + self.list[data]["iconId"] + ".png")
            icon.thumbnail((20, 20), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(icon)
            self.list[data]["icon"] = icon
            self.list[data]["need"] = results.get(data)
            self.list[data]["have"] = iFrame.InventoryFrame.frames[data].itemHave.get()
        for i in self.results.get_children():
            self.results.delete(i)
        if results:
            for i in results:
                self.results.insert("", tk.END, image=self.list[i]["icon"],
                                    values=(self.list[i]["name"], self.list[i]["need"], self.list[i]["have"]))

    def add_ear_to_list(self):
        """
        По нажатию кнопки Add Operator добавляет ушку в список на прокачку и в словарик объектов с ушками на прокачку.
        """
        earlist_copy = self.allEarsList.copy()
        name = self.selectOperator.get()
        results = self.create_upgrade_string(self.currentStats.construct_op(), self.desiredStats.construct_op())
        if results:
            if earlist_copy.get(name):
                ear = self.allEarsList.get(name)
                self.earsList.delete(ear.iid)
                self.allEarsList.pop(name)
                iid = self.earsList.insert("", tk.END, values=(self.selectOperator.get(), results))
                operator = ADP.OperatorState(iid, self.selectOperator.get(),
                                             self.currentStats.construct_op(),
                                             self.desiredStats.construct_op())
                self.allEarsList.setdefault(operator.name)
                self.allEarsList[operator.name] = operator
            else:
                iid = self.earsList.insert("", tk.END, values=(self.selectOperator.get(), results))
                operator = ADP.OperatorState(iid, self.selectOperator.get(),
                                             self.currentStats.construct_op(),
                                             self.desiredStats.construct_op())
                self.allEarsList.setdefault(operator.name)
                self.allEarsList[operator.name] = operator
        # self.create_path_list()

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

    def del_ear_from_list(self):
        """
        По нажатию кнопки Delete Operator удаляет ушку из таблички ушек и из словарика ушек.
        """
        for i in self.results.get_children():
            self.results.delete(i)
        for s in self.earsList.selection():
            name = self.earsList.item(s)
            values = name.get('values')
            self.earsList.delete(s)
            self.allEarsList.pop(values[0])
        # self.create_path_list()

    def del_all_ears(self):
        for ear in self.earsList.get_children():
            self.earsList.delete(ear)
        self.allEarsList = {}

    # noinspection PyUnusedLocal
    def set_max_lvls(self, event):
        """
        Выполняет установку ограничений для полей ввода параметров ушки.
        :param event: Принимает на вход event.
        """
        ear = ADP.Operator(self.selectOperator.get())
        self.currentStats.clear_spinboxes()
        self.desiredStats.clear_spinboxes()
        self.currentStats.callback()
        self.desiredStats.callback()
        self.skills_counter(ear.ear["skills"])

    def skills_counter(self, skills):
        """
        Управляет работой полей ввода, отключая ненужные в зависимости от редкости ушки.
        :param skills: Принимает на вход массив skills ушки, рассчитывая на его основе количество навыков ушки.
        """
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
