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
        self.view.selectElite.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"\d")),
                                        invalidcommand=(self.ivcmd, "%P", "%W"))
        self.view.selectLvl.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"\d{1,2}")),
                                      invalidcommand=(self.ivcmd, "%P", "%W"))
        self.view.selectSkill1.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"10|\d")),
                                         invalidcommand=(self.ivcmd, "%P", "%W"))
        self.view.selectSkill2.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"10|\d")),
                                         invalidcommand=(self.ivcmd, "%P", "%W"))
        self.view.selectSkill3.configure(validate="all", validatecommand=(self.vcmd, "%P", "%W", str(""r"10|\d")),
                                         invalidcommand=(self.ivcmd, "%P", "%W"))

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

    def get_ear(self, name):
        return operator.Operator(name)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def set_binds(self):
        self.view.selectElite.bind("<Any-KeyRelease>", self.on_reset)
        self.view.selectSkill1.bind("<Any-KeyRelease>", self.sync_spinbox)
        self.view.selectSkill2.bind("<Any-KeyRelease>", self.sync_spinbox)
        self.view.selectSkill3.bind("<Any-KeyRelease>", self.sync_spinbox)
        self.view.selectSkill3.configure(command=lambda: self.sync_spinbox(self.view.selectSkill3.get()))
        self.view.selectSkill2.configure(command=lambda: self.sync_spinbox(self.view.selectSkill2.get()))
        self.view.selectSkill1.configure(command=lambda: self.sync_spinbox(self.view.selectSkill1.get()))
        self.view.selectElite.configure(command=lambda: self.on_reset(""))

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

    def clear_spinboxes(self):
        """
        Очищает все поля, сбрасывая их к изначальным значениям.
        """
        self.view.selectElite.delete(0, 9)
        self.view.selectElite.insert(0, "0")
        self.view.selectLvl.delete(0, 9)
        self.view.selectLvl.insert(0, "1")
        self.view.selectSkill1.delete(0, 9)
        self.view.selectSkill2.delete(0, 9)
        self.view.selectSkill3.delete(0, 9)
        self.view.selectSkill1.insert(0, "1")
        self.view.selectSkill2.insert(0, "1")
        self.view.selectSkill3.insert(0, "1")

    def on_update(self):
        """
        Обновляет фрейм, задавая ограничения полям для ввода на основе выбранной ушки.
        """
        ear = self.model.get_ear(self.view.master.master.selectOperator.get())
        self.view.selectElite["to"] = len(ear.ear["phases"]) - 1
        self.view.selectLvl["to"] = int(ear.phase(self.view.selectElite.get()))
        if self.view.selectLvl["to"] <= int(self.view.selectLvl.get()):
            self.view.selectLvl.delete(0, 9)
            self.view.selectLvl.insert(0, self.view.selectLvl["to"])
        self.view.selectSkill1["to"] = ear.skill_lvl(self.view.selectElite.get())
        self.view.selectSkill2["to"] = ear.skill_lvl(self.view.selectElite.get())
        self.view.selectSkill3["to"] = ear.skill_lvl(self.view.selectElite.get())

    def sync_spinbox(self, event):
        """
        Синхронизирует ввод для полей, отвещающих за уровни навыков ушки.
        :param event:
        """
        if type(event) == tk.Event:
            sbvalue = event.widget.get()
        else:
            sbvalue = event
        if int(sbvalue) <= 7:
            self.view.selectSkill1.delete(0, 9)
            self.view.selectSkill1.insert(0, sbvalue)
            self.view.selectSkill2.delete(0, 9)
            self.view.selectSkill2.insert(0, sbvalue)
            self.view.selectSkill3.delete(0, 9)
            self.view.selectSkill3.insert(0, sbvalue)

    def on_reset(self, event):
        """
        Сбрасывает поля ввода при изменении уровня элитки ушки.
        :param event: Принимает на вход event.
        """
        self.on_update()
        if int(self.view.selectLvl.get()) > self.view.selectLvl["to"]:
            self.view.selectLvl.delete(0, 9)
            self.view.selectLvl.insert(0, self.view.selectLvl["to"])
        if int(self.view.selectSkill1.get()) > self.view.selectSkill1["to"]:
            self.view.selectSkill1.delete(0, 9)
            self.view.selectSkill2.delete(0, 9)
            self.view.selectSkill3.delete(0, 9)
            self.view.selectSkill1.insert(0, self.view.selectSkill1["to"])
            self.view.selectSkill2.insert(0, self.view.selectSkill1["to"])
            self.view.selectSkill3.insert(0, self.view.selectSkill1["to"])

    def skills_counter(self, skills):
        """
        Управляет работой полей ввода, отключая ненужные в зависимости от редкости ушки.
        :param skills: Принимает на вход массив skills ушки, рассчитывая на его основе количество навыков ушки.
        """
        self.view.selectSkill1.configure(state="disabled")
        self.view.selectSkill2.configure(state="disabled")
        self.view.selectSkill3.configure(state="disabled")
        if len(skills) >= 1:
            self.view.selectSkill1.configure(state="normal")
        if len(skills) >= 2:
            self.view.selectSkill2.configure(state="normal")
        if len(skills) == 3:
            self.view.selectSkill3.configure(state="normal")

    def set_params(self, skills):
        self.clear_spinboxes()
        self.skills_counter(skills)


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

        self.controller.set_binds()
