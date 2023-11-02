# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import *
from tkinter import ttk

from data_parser.inventory import Inventory
from data_parser.planner_logic import PlannerLogic


class View(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.controller = None

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.text = StringVar()
        self.label = tk.Label(self, justify="left", textvariable=self.text)
        self.label.grid(column=0, row=0, sticky="ew")
        self.text.set("Total items sanity cost: 0")

        self.calculateFrame = ttk.Treeview(self, columns=["name", "need", "cost", "runs", "stage"])
        self.calculateFrame.grid(column=0, row=1, sticky="nsew")
        self.calculateFrame.column("#0", stretch=False, width=150)
        self.calculateFrame.heading("#0", text="Icon", anchor="center")
        self.calculateFrame.column("name", stretch=True, width=150)
        self.calculateFrame.heading("name", text="Item", anchor="center")
        self.calculateFrame.column("need", stretch=True, width=70)
        self.calculateFrame.heading("need", text="Need", anchor="center")
        self.calculateFrame.column("cost", stretch=True, width=70)
        self.calculateFrame.heading("cost", text="Cost (sum)", anchor="center")
        self.calculateFrame.column("runs", stretch=True, width=70)
        self.calculateFrame.heading("runs", text="Runs", anchor="center")
        self.calculateFrame.column("stage", stretch=True, width=150)
        self.calculateFrame.heading("stage", text="Stage", anchor="center")
        self.calculateFrame.tag_configure('comp', background='Yellow')
        self.calculateFrame.tag_configure('farm', background='Red')

    def set_controller(self, controller):
        self.controller = controller


class Model:
    def __init__(self):
        pass

    @staticmethod
    def get_inventory():
        return Inventory().inventory.copy()


class Controller:
    def __init__(self, model, view):

        self.model = model
        self.view = view

    def clear_all(self):
        self.view.calculateFrame.delete(*self.view.calculateFrame.get_children())


class OverallPathFrame():
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.view = View(master=master)
        self.model = Model()
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)

        self.results = PlannerLogic()