import tkinter as tk
from tkinter import ttk
from tkinter import *
import plannerPanels
import ArknightsDataParser


class Planner(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)
        self.master = master

        self.ear = 0
        self.earsListDict = {}

        self.selectOperator = ttk.Combobox(self)
        self.selectOperator.insert(0, "Nearl")
        self.selectOperator["values"] = ArknightsDataParser.returnListofEars()
        self.selectOperator.grid(row=0, columnspan=2, padx=3, pady=(3, 10), sticky="ew")
        self.selectOperator.bind("<<ComboboxSelected>>", self.set_max_lvls)

        self.currentStats = plannerPanels.Panel(self)
        self.currentStats.grid(column=0, row=1, padx=3, sticky="nsew")

        self.desiredStats = plannerPanels.Panel(self)
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
        self.earsList.bind("<<TreeviewSelect>>", self.calculate)

        self.leftFrame = tk.Frame(self)
        self.leftFrame.grid(column=1, row=3, sticky="nsew", pady=(6, 0), padx=(3, 0))
        self.leftFrame.columnconfigure(0, weight=1)
        self.leftFrame.rowconfigure(0, weight=1)

        # self.results = ttk.Listbox(self.leftFrame, relief="sunken", bg="#FFFFFF", justify="left", activestyle='none',
        #                           takefocus=0, selectmode=tk.EXTENDED)
        self.results = ttk.Treeview(self.leftFrame, columns=["name", "count"])
        self.results.grid(column=0, row=0, sticky="nsew")
        self.results.column("#0", stretch=False, width=75)
        self.results.heading("#0", text="Icon", anchor="center")
        self.results.column("name", stretch=True, width=100)
        self.results.heading("name", text="Item", anchor="center")
        self.results.column("count", stretch=True, width=100)
        self.results.heading("count", text="Count", anchor="center")
        # self.results["width"] = self.leftFrame.winfo_width()
        # self.results["height"] = self.leftFrame.winfo_height()

        self.set_max_lvls("")

    def calculate_button(self):
        self.calculate("")

    def calculate(self, event):
        results = {}
        tpl = self.earsList.selection()
        for s in tpl:
            selection = self.earsList.item(s)
            values = selection.get('values')
            name = values[0]
            for ear in self.earsListDict.values():
                if ear.name == name:
                    self.ear = ear
                    break
            # operator = ArknightsDataParser.OperatorState(self.ear.name, self.ear.current, self.ear.desired)
            items = ArknightsDataParser.calculate(self.ear)
            if items:
                for i in items.items():
                    count = results.get(i[0], 0)
                    results[i[0]] = count + i[1]
        for i in self.results.get_children():
            self.results.delete(i)
        if results:
            for i in results:
                self.results.insert("", tk.END, values=(i, results.get(i)))

    # (i + " : " + str(results.get(i))

    def add_ear_to_list(self):
        earlist_copy = self.earsListDict.copy()
        name = self.selectOperator.get()
        results = self.create_upgrade_string()
        if results:
            if earlist_copy.get(name):
                ear = self.earsListDict.get(name)
                self.earsList.delete(ear.iid)
                self.earsListDict.pop(name)
                iid = self.earsList.insert("", tk.END, values=(self.selectOperator.get(), results))
                operator = ArknightsDataParser.OperatorState(iid, self.selectOperator.get(),
                                                             self.currentStats.construct_op(),
                                                             self.desiredStats.construct_op())
                self.earsListDict.setdefault(operator.name)
                self.earsListDict[operator.name] = operator
            else:
                iid = self.earsList.insert("", tk.END, values=(self.selectOperator.get(), results))
                operator = ArknightsDataParser.OperatorState(iid, self.selectOperator.get(),
                                                             self.currentStats.construct_op(),
                                                             self.desiredStats.construct_op())
                self.earsListDict.setdefault(operator.name)
                self.earsListDict[operator.name] = operator

    def create_upgrade_string(self):
        current = self.currentStats
        desired = self.desiredStats
        results = ""
        if int(current.selectElite.get()) < int(desired.selectElite.get()):
            results += (str(current.selectElite.get()) + "e" + str(current.selectLvl.get()) + " >>> "
                        + str(desired.selectElite.get()) + "e" + str(desired.selectLvl.get()) + "; ")
        if (int(current.selectElite.get()) == int(desired.selectElite.get())) and (
                int(current.selectLvl.get()) < int(desired.selectLvl.get())):
            results += (str(current.selectElite.get()) + "e" + str(current.selectLvl.get()) + " >>> "
                        + str(desired.selectElite.get()) + "e" + str(desired.selectLvl.get()) + "; ")
        if int(current.selectSkill1.get()) < int(desired.selectSkill1.get()):
            results += ("S1(" + str(current.selectSkill1.get()) + " to " + str(desired.selectSkill1.get()) + "); ")
        if int(current.selectSkill2.get()) < int(desired.selectSkill2.get()):
            results += ("S2(" + str(current.selectSkill2.get()) + " to " + str(desired.selectSkill2.get()) + "); ")
        if int(current.selectSkill3.get()) < int(desired.selectSkill3.get()):
            results += ("S3(" + str(current.selectSkill3.get()) + " to " + str(desired.selectSkill3.get()) + "); ")
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
            self.earsListDict.pop(values[0])

    def set_max_lvls(self, event):
        ear = ArknightsDataParser.Operator(self.selectOperator.get())
        self.currentStats.clear_spinboxes()
        self.desiredStats.clear_spinboxes()
        self.currentStats.callback()
        self.desiredStats.callback()
        if 0 <= ear.rarity <= 1:
            self.currentStats.selectSkill1.configure(state=DISABLED)
            self.currentStats.selectSkill2.configure(state=DISABLED)
            self.currentStats.selectSkill3.configure(state=DISABLED)
            self.desiredStats.selectSkill1.configure(state=DISABLED)
            self.desiredStats.selectSkill2.configure(state=DISABLED)
            self.desiredStats.selectSkill3.configure(state=DISABLED)
        if ear.rarity == 2:
            self.currentStats.selectSkill1.configure(state=NORMAL)
            self.currentStats.selectSkill2.configure(state=DISABLED)
            self.currentStats.selectSkill3.configure(state=DISABLED)
            self.desiredStats.selectSkill1.configure(state=NORMAL)
            self.desiredStats.selectSkill2.configure(state=DISABLED)
            self.desiredStats.selectSkill3.configure(state=DISABLED)
        if 3 <= ear.rarity <= 4:
            self.currentStats.selectSkill1.configure(state=NORMAL)
            self.currentStats.selectSkill2.configure(state=NORMAL)
            self.currentStats.selectSkill3.configure(state=DISABLED)
            self.desiredStats.selectSkill1.configure(state=NORMAL)
            self.desiredStats.selectSkill2.configure(state=NORMAL)
            self.desiredStats.selectSkill3.configure(state=DISABLED)
        if ear.rarity == 5:
            self.currentStats.selectSkill1.configure(state=NORMAL)
            self.currentStats.selectSkill2.configure(state=NORMAL)
            self.currentStats.selectSkill3.configure(state=NORMAL)
            self.desiredStats.selectSkill1.configure(state=NORMAL)
            self.desiredStats.selectSkill2.configure(state=NORMAL)
            self.desiredStats.selectSkill3.configure(state=NORMAL)

