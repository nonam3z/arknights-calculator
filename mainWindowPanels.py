import tkinter as tk
from tkinter import ttk
from tkinter import *
import ArknightsDataParser
import PenguinLogisticsParser


class Panel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.columnconfigure(1, weight=1)

        self.ear = 0
        self.master = master

        tk.Label(self, justify="left", text="Elite", width=5).grid(column=0, row=0)
        tk.Label(self, justify="left", text="Level", width=5).grid(column=0, row=1)
        tk.Label(self, justify="left", text="Skill 1", width=5).grid(column=0, row=2)
        tk.Label(self, justify="left", text="Skill 2", width=5).grid(column=0, row=3)
        tk.Label(self, justify="left", text="Skill 3", width=5).grid(column=0, row=4)

        self.selectElite = ttk.Spinbox(self, from_=0, to=2, command=self.callback)
        self.selectElite.grid(column=1, row=0, sticky="ew")
        self.selectElite.insert(0, "0")

        self.selectLvl = ttk.Spinbox(self, from_=1, to=90)
        self.selectLvl.grid(column=1, row=1, sticky="ew")
        self.selectLvl.insert(0, "1")

        self.selectSkill1 = ttk.Spinbox(self, from_=1, to=10, command=self.sync_spinbox1)
        self.selectSkill1.grid(column=1, row=2, sticky="ew")
        self.selectSkill1.insert(0, "1")

        self.selectSkill2 = ttk.Spinbox(self, from_=1, to=10, command=self.sync_spinbox2)
        self.selectSkill2.grid(column=1, row=3, sticky="ew")
        self.selectSkill2.insert(0, "1")

        self.selectSkill3 = ttk.Spinbox(self, from_=1, to=10, command=self.sync_spinbox3)
        self.selectSkill3.grid(column=1, row=4, sticky="ew")
        self.selectSkill3.insert(0, "1")

    def construct_op(self):
        elite = self.selectElite.get()
        level = self.selectLvl.get()
        skill1 = self.selectSkill1.get()
        skill2 = self.selectSkill2.get()
        skill3 = self.selectSkill3.get()
        return ArknightsDataParser.Stats(int(elite), int(level), int(skill1), int(skill2), int(skill3))

    def on_update(self):
        self.ear = ArknightsDataParser.Operator(self.master.selectOperator.get())
        self.selectElite["to"] = self.ear.maxElite
        if self.selectElite["to"] <= int(self.selectElite.get()):
            self.selectElite.delete(0, 9)
            self.selectElite.insert(0, self.selectElite["to"])
        self.selectLvl["to"] = int(self.ear.phase(self.selectElite.get()))
        if self.selectLvl["to"] <= int(self.selectLvl.get()):
            self.selectLvl.delete(0, 9)
            self.selectLvl.insert(0, self.selectLvl["to"])
        self.selectSkill1["to"] = self.ear.skillLvl(self.selectElite.get())
        self.selectSkill2["to"] = self.ear.skillLvl(self.selectElite.get())
        self.selectSkill3["to"] = self.ear.skillLvl(self.selectElite.get())

    def sync_spinbox1(self):
        if (self.selectSkill2.get() and self.selectSkill3.get()) <= self.selectSkill1.get() <= str(
                7) and self.selectSkill1.get() != str(10):
            self.selectSkill2.delete(0, 9)
            self.selectSkill2.insert(0, self.selectSkill1.get())
            self.selectSkill3.delete(0, 9)
            self.selectSkill3.insert(0, self.selectSkill1.get())
        if (self.selectSkill2.get() and self.selectSkill3.get()) >= self.selectSkill1.get() <= str(
                7) and self.selectSkill1.get() != str(10):
            self.selectSkill2.delete(0, 9)
            self.selectSkill2.insert(0, self.selectSkill1.get())
            self.selectSkill3.delete(0, 9)
            self.selectSkill3.insert(0, self.selectSkill1.get())

    def sync_spinbox2(self):
        if (self.selectSkill1.get() and self.selectSkill3.get()) <= self.selectSkill2.get() <= str(
                7) and self.selectSkill2.get() != str(10):
            self.selectSkill1.delete(0, 9)
            self.selectSkill1.insert(0, self.selectSkill2.get())
            self.selectSkill3.delete(0, 9)
            self.selectSkill3.insert(0, self.selectSkill2.get())
        if (self.selectSkill1.get() and self.selectSkill3.get()) >= self.selectSkill2.get() <= str(
                7) and self.selectSkill2.get() != str(10):
            self.selectSkill1.delete(0, 9)
            self.selectSkill1.insert(0, self.selectSkill2.get())
            self.selectSkill3.delete(0, 9)
            self.selectSkill3.insert(0, self.selectSkill2.get())

    def sync_spinbox3(self):
        if (self.selectSkill1.get() and self.selectSkill2.get()) >= self.selectSkill3.get() <= str(
                7) and self.selectSkill3.get() != str(10):
            self.selectSkill1.delete(0, 9)
            self.selectSkill1.insert(0, self.selectSkill3.get())
            self.selectSkill2.delete(0, 9)
            self.selectSkill2.insert(0, self.selectSkill3.get())
        if (self.selectSkill1.get() and self.selectSkill2.get()) <= self.selectSkill3.get() <= str(
                7) and self.selectSkill3.get() != str(10):
            self.selectSkill1.delete(0, 9)
            self.selectSkill1.insert(0, self.selectSkill3.get())
            self.selectSkill2.delete(0, 9)
            self.selectSkill2.insert(0, self.selectSkill3.get())

    def on_reset(self, event):
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
        self.selectElite.delete(0, 9)
        self.selectElite.insert(0, 0)
        self.selectLvl.delete(0, 9)
        self.selectLvl.insert(0, 1)
        self.selectSkill1.delete(0, 9)
        self.selectSkill2.delete(0, 9)
        self.selectSkill3.delete(0, 9)
        self.selectSkill1.insert(0, 1)
        self.selectSkill2.insert(0, 1)
        self.selectSkill3.insert(0, 1)

    def callback(self):
        self.on_reset("")
