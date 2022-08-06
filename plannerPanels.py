import re
import tkinter
import tkinter as tk
from tkinter import ttk

import ArknightsDataParser


class CalcPanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.columnconfigure(1, weight=1)

        self.ear = ""
        self.master = master

        tk.Label(self, justify="left", text="Elite", width=5).grid(column=0, row=0)
        tk.Label(self, justify="left", text="Level", width=5).grid(column=0, row=1)
        tk.Label(self, justify="left", text="Skill 1", width=5).grid(column=0, row=2)
        tk.Label(self, justify="left", text="Skill 2", width=5).grid(column=0, row=3)
        tk.Label(self, justify="left", text="Skill 3", width=5).grid(column=0, row=4)

        self.vcmdElite = (self.register(self.validateElite), "%P", "%W")
        self.vcmdLvl = (self.register(self.validateLvl), "%P", "%W")
        self.vcmdSkill = (self.register(self.validateSkill), "%P", "%W")
        self.ivcmd = (self.register(self.onInvalid), "%W", "%P")

        self.selectElite = ttk.Spinbox(self, from_=0, to=2)
        self.selectElite.insert(0, "0")
        self.selectElite.configure(command=lambda: self.callback("<Command event.>"))
        self.selectElite.configure(validate="all", validatecommand=self.vcmdElite, invalidcommand=self.ivcmd)
        self.selectElite.grid(column=1, row=0, sticky="ew")

        self.selectLvl = ttk.Spinbox(self, from_=1, to=90)
        self.selectLvl.insert(0, "1")
        self.selectLvl.configure(validate="all", validatecommand=self.vcmdLvl, invalidcommand=self.ivcmd)
        self.selectLvl.grid(column=1, row=1, sticky="ew")

        self.selectSkill1 = ttk.Spinbox(self, from_=1, to=10)
        self.selectSkill1.insert(0, "1")
        self.selectSkill1.configure(command=lambda: self.sync_spinbox(self.selectSkill1.get()))
        self.selectSkill1.configure(validate="all", validatecommand=self.vcmdSkill, invalidcommand=self.ivcmd)
        self.selectSkill1.grid(column=1, row=2, sticky="ew")

        self.selectSkill2 = ttk.Spinbox(self, from_=1, to=10)
        self.selectSkill2.insert(0, "1")
        self.selectSkill2.configure(command=lambda: self.sync_spinbox(self.selectSkill2.get()))
        self.selectSkill2.configure(validate="all", validatecommand=self.vcmdSkill, invalidcommand=self.ivcmd)
        self.selectSkill2.grid(column=1, row=3, sticky="ew")

        self.selectSkill3 = ttk.Spinbox(self, from_=1, to=10)
        self.selectSkill3.insert(0, "1")
        self.selectSkill3.configure(command=lambda: self.sync_spinbox(self.selectSkill3.get()))
        self.selectSkill3.configure(validate="all", validatecommand=self.vcmdSkill, invalidcommand=self.ivcmd)
        self.selectSkill3.grid(column=1, row=4, sticky="ew")

        self.selectElite.bind("<Any-KeyRelease>", self.callback)
        self.selectSkill1.bind("<Any-KeyRelease>", self.sync_spinbox)
        self.selectSkill2.bind("<Any-KeyRelease>", self.sync_spinbox)
        self.selectSkill3.bind("<Any-KeyRelease>", self.sync_spinbox)

    def validateElite(self, P, W):
        widget = self.master.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        pattern_elite = r"\d"
        try:
            if P == "":
                return True
            if (_from <= int(P) <= _to) and re.fullmatch(pattern_elite, P):
                return True
        except ValueError:
            return False
        return False

    def validateLvl(self, P, W):
        widget = self.master.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        pattern_level = r"\d{1,2}"
        try:
            if P == "":
                return True
            if (_from <= int(P) <= _to) and re.fullmatch(pattern_level, P):
                return True
        except ValueError:
            return False
        return False

    def validateSkill(self, P, W):
        widget = self.master.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        pattern_skills = r"10|\d"
        try:
            if P == "":
                return True
            if (_from <= int(P) <= _to) and re.fullmatch(pattern_skills, P):
                return True
        except ValueError:
            return False
        return False

    def onInvalid(self, W, P):
        widget = self.master.nametowidget(W)
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

    def construct_op(self):
        """
        Создаем объект-ушку с заданными параметрами на прокачку.
        :return: Возвращает ушку как объект с параметрами для прокачки.
        """
        elite = self.selectElite.get()
        level = self.selectLvl.get()
        skill1 = self.selectSkill1.get()
        skill2 = self.selectSkill2.get()
        skill3 = self.selectSkill3.get()
        return ArknightsDataParser.Stats(int(elite), int(level), int(skill1), int(skill2), int(skill3))

    def on_update(self):
        """
        Обновляет фрейм, задавая ограничения полям для ввода на основе выбранной ушки.
        """
        self.ear = ArknightsDataParser.Operator(self.master.selectOperator.get())
        self.selectElite["to"] = len(self.ear.ear["phases"]) - 1
        self.selectLvl["to"] = int(self.ear.phase(self.selectElite.get()))
        if self.selectLvl["to"] <= int(self.selectLvl.get()):
            self.selectLvl.delete(0, 9)
            self.selectLvl.insert(0, self.selectLvl["to"])
        self.selectSkill1["to"] = self.ear.skill_lvl(self.selectElite.get())
        self.selectSkill2["to"] = self.ear.skill_lvl(self.selectElite.get())
        self.selectSkill3["to"] = self.ear.skill_lvl(self.selectElite.get())

    def sync_spinbox(self, event):
        """
        Синхронизирует ввод для полей, отвещающих за уровни навыков ушки.
        :param event:
        """
        print("Sync spinbox triggered: " + str(event))
        if type(event) == tkinter.Event:
            sbvalue = event.widget.get()
        else:
            sbvalue = event
        if int(sbvalue) <= 7:
            self.selectSkill1.delete(0, 9)
            self.selectSkill1.insert(0, sbvalue)
            self.selectSkill2.delete(0, 9)
            self.selectSkill2.insert(0, sbvalue)
            self.selectSkill3.delete(0, 9)
            self.selectSkill3.insert(0, sbvalue)

    # noinspection PyUnusedLocal
    def on_reset(self, event):
        """
        Сбрасывает поля ввода при изменении уровня элитки ушки.
        :param event: Принимает на вход event.
        """
        self.on_update()
        if int(self.selectLvl.get()) > self.selectLvl["to"]:
            self.selectLvl.delete(0, 9)
            self.selectLvl.insert(0, self.selectLvl["to"])
        if int(self.selectSkill1.get()) > self.selectSkill1["to"]:
            self.selectSkill1.delete(0, 9)
            self.selectSkill2.delete(0, 9)
            self.selectSkill3.delete(0, 9)
            self.selectSkill1.insert(0, self.selectSkill1["to"])
            self.selectSkill2.insert(0, self.selectSkill1["to"])
            self.selectSkill3.insert(0, self.selectSkill1["to"])

    def clear_spinboxes(self):
        """
        Очищает все поля, сбрасывая их к изначальным значениям.
        """
        self.selectElite.delete(0, 9)
        self.selectElite.insert(0, "0")
        self.selectLvl.delete(0, 9)
        self.selectLvl.insert(0, "1")
        self.selectSkill1.delete(0, 9)
        self.selectSkill2.delete(0, 9)
        self.selectSkill3.delete(0, 9)
        self.selectSkill1.insert(0, "1")
        self.selectSkill2.insert(0, "1")
        self.selectSkill3.insert(0, "1")

    def callback(self, event):
        print("Callback triggered: " + str(event))
        self.on_reset("")
