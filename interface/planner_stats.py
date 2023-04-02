# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import re
import tkinter as tk
from tkinter import ttk

from data_parser import operator


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.columnconfigure(1, weight=1)

        self.controller = None

        self.ear = ""

        tk.Label(self, justify="left", text="Elite", width=6).grid(column=0, row=0)
        tk.Label(self, justify="left", text="Level", width=6).grid(column=0, row=1)
        tk.Label(self, justify="left", text="Skill 1", width=6).grid(column=0, row=2)
        tk.Label(self, justify="left", text="Skill 2", width=6).grid(column=0, row=3)
        tk.Label(self, justify="left", text="Skill 3", width=6).grid(column=0, row=4)

        self.selectElite = ttk.Spinbox(self, from_=0, to=2)
        self.selectElite.insert(0, "0")
        self.selectElite.grid(column=1, row=0, sticky="ew")

        self.selectLvl = ttk.Spinbox(self, from_=1, to=90)
        self.selectLvl.insert(0, "1")
        self.selectLvl.grid(column=1, row=1, sticky="ew")

        self.selectSkill1 = ttk.Spinbox(self, from_=1, to=10)
        self.selectSkill1.insert(0, "1")
        self.selectSkill1.grid(column=1, row=2, sticky="ew")

        self.selectSkill2 = ttk.Spinbox(self, from_=1, to=10)
        self.selectSkill2.insert(0, "1")
        self.selectSkill2.grid(column=1, row=3, sticky="ew")

        self.selectSkill3 = ttk.Spinbox(self, from_=1, to=10)
        self.selectSkill3.insert(0, "1")
        self.selectSkill3.grid(column=1, row=4, sticky="ew")

    def set_controller(self, controller):
        self.controller = controller


class ValidateModel:
    def __init__(self, view):
        self.view = view

        self.vcmd = (self.view.register(self.validate))
        self.ivcmd = (self.view.register(self.onInvalid))

    def set_validate(self):
        self.view.selectElite.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"\d")), invalidcommand=self.ivcmd)
        self.view.selectLvl.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"\d{1,2}")), invalidcommand=self.ivcmd)
        self.view.selectSkill1.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"10|\d")), invalidcommand=self.ivcmd)
        self.view.selectSkill2.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"10|\d")), invalidcommand=self.ivcmd)
        self.view.selectSkill3.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"10|\d")), invalidcommand=self.ivcmd)

    def validate(self, P, W, pattern):
        widget = self.view.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        try:
            if P == "":
                return True
            if (_from <= int(P) <= _to) and re.fullmatch(pattern, P):
                return True
        except ValueError:
            return False
        return False

    def onInvalid(self, P, W):
        widget = self.view.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        widget.delete(0, 9)
        try:
            if P.isdigit():
                if int(P) >= _to:
                    widget.insert(0, _to)
                if int(P) <= _from:
                    widget.insert(0, _from)
            else:
                widget.insert(0, _from)
        except ValueError:
            widget.insert(0, _from)


class Model:
    def __init__(self):
        pass


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def construct_op(self):
        """
        Создаем объект-ушку с заданными параметрами на прокачку.
        :return: Возвращает ушку как объект с параметрами для прокачки.
        """
        elite = self.view.selectElite.get()
        level = self.view.selectLvl.get()
        skill1 = self.view.selectSkill1.get()
        skill2 = self.view.selectSkill2.get()
        skill3 = self.view.selectSkill3.get()
        return operator.Stats(int(elite), int(level), int(skill1), int(skill2), int(skill3))


class StatsPanel:
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.view = View(master=master)
        self.model = Model()
        self.validate = ValidateModel(self.view)
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)
        self.validate.set_validate()


        # self.selectElite.bind("<Any-KeyRelease>", self.callback)
        # self.selectSkill1.bind("<Any-KeyRelease>", self.sync_spinbox)
        # self.selectSkill2.bind("<Any-KeyRelease>", self.sync_spinbox)
        # self.selectSkill3.bind("<Any-KeyRelease>", self.sync_spinbox)
        # self.selectSkill3.configure(command=lambda: self.sync_spinbox(self.selectSkill3.get()))
        # self.selectSkill2.configure(command=lambda: self.sync_spinbox(self.selectSkill2.get()))
        # self.selectSkill1.configure(command=lambda: self.sync_spinbox(self.selectSkill1.get()))
        # self.selectElite.configure(command=lambda: self.callback("<Command event.>"))

        # def construct_op(self):
        #     """
        #     Создаем объект-ушку с заданными параметрами на прокачку.
        #     :return: Возвращает ушку как объект с параметрами для прокачки.
        #     """
        #     elite = self.selectElite.get()
        #     level = self.selectLvl.get()
        #     skill1 = self.selectSkill1.get()
        #     skill2 = self.selectSkill2.get()
        #     skill3 = self.selectSkill3.get()
        #     return files_loader.Stats(int(elite), int(level), int(skill1), int(skill2), int(skill3))
        #
        # def on_update(self):
        #     """
        #     Обновляет фрейм, задавая ограничения полям для ввода на основе выбранной ушки.
        #     """
        #     self.ear = files_loader.Operator(self.master.selectOperator.get())
        #     self.selectElite["to"] = len(self.ear.ear["phases"]) - 1
        #     self.selectLvl["to"] = int(self.ear.phase(self.selectElite.get()))
        #     if self.selectLvl["to"] <= int(self.selectLvl.get()):
        #         self.selectLvl.delete(0, 9)
        #         self.selectLvl.insert(0, self.selectLvl["to"])
        #     self.selectSkill1["to"] = self.ear.skill_lvl(self.selectElite.get())
        #     self.selectSkill2["to"] = self.ear.skill_lvl(self.selectElite.get())
        #     self.selectSkill3["to"] = self.ear.skill_lvl(self.selectElite.get())
        #
        # def sync_spinbox(self, event):
        #     """
        #     Синхронизирует ввод для полей, отвещающих за уровни навыков ушки.
        #     :param event:
        #     """
        #     print("Sync spinbox triggered: " + str(event))
        #     if type(event) == tkinter.Event:
        #         sbvalue = event.widget.get()
        #     else:
        #         sbvalue = event
        #     if int(sbvalue) <= 7:
        #         self.selectSkill1.delete(0, 9)
        #         self.selectSkill1.insert(0, sbvalue)
        #         self.selectSkill2.delete(0, 9)
        #         self.selectSkill2.insert(0, sbvalue)
        #         self.selectSkill3.delete(0, 9)
        #         self.selectSkill3.insert(0, sbvalue)
        #
        # # noinspection PyUnusedLocal
        # def on_reset(self, event):
        #     """
        #     Сбрасывает поля ввода при изменении уровня элитки ушки.
        #     :param event: Принимает на вход event.
        #     """
        #     self.on_update()
        #     if int(self.selectLvl.get()) > self.selectLvl["to"]:
        #         self.selectLvl.delete(0, 9)
        #         self.selectLvl.insert(0, self.selectLvl["to"])
        #     if int(self.selectSkill1.get()) > self.selectSkill1["to"]:
        #         self.selectSkill1.delete(0, 9)
        #         self.selectSkill2.delete(0, 9)
        #         self.selectSkill3.delete(0, 9)
        #         self.selectSkill1.insert(0, self.selectSkill1["to"])
        #         self.selectSkill2.insert(0, self.selectSkill1["to"])
        #         self.selectSkill3.insert(0, self.selectSkill1["to"])
        #
        # def clear_spinboxes(self):
        #     """
        #     Очищает все поля, сбрасывая их к изначальным значениям.
        #     """
        #     self.selectElite.delete(0, 9)
        #     self.selectElite.insert(0, "0")
        #     self.selectLvl.delete(0, 9)
        #     self.selectLvl.insert(0, "1")
        #     self.selectSkill1.delete(0, 9)
        #     self.selectSkill2.delete(0, 9)
        #     self.selectSkill3.delete(0, 9)
        #     self.selectSkill1.insert(0, "1")
        #     self.selectSkill2.insert(0, "1")
        #     self.selectSkill3.insert(0, "1")
        #
        # def callback(self, event):
        #     # print("Callback triggered: " + str(event))
        #     self.on_reset("")
