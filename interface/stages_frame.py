# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import ttk

import ttkwidgets as ttkw

import data_parser.stages


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.controller = None

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.selectAll = ttk.Button(self, text="Select All")
        self.selectAll.grid(column=0, row=0)

        self.stagesFrame = ttkw.CheckboxTreeview(self, columns=["name", "stageId"])
        self.stagesFrame.grid(column=0, row=1, sticky="nsew")
        self.stagesFrame.column("#0", stretch=False, width=150)
        self.stagesFrame.heading("#0", text="Icon", anchor="center")
        self.stagesFrame.column("name", stretch=True, width=150)
        self.stagesFrame.heading("name", text="Name", anchor="center")
        self.stagesFrame.column("stageId", stretch=True, width=150)
        self.stagesFrame.heading("stageId", text="Stage Id", anchor="center")

    def set_controller(self, controller):
        self.controller = controller


class Model():
    def __init__(self):
        pass


class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model

    def select_all(self):
        for iid in self.view.stagesFrame.get_children():
            self.view.stagesFrame.change_state(iid, "checked")
            for child_iid in self.view.stagesFrame.get_children(iid):
                self.view.stagesFrame.change_state(child_iid, "checked")

    def get_checked_stages(self):
        allowed_stages_iid = list(self.view.stagesFrame.tag_has("checked"))
        allowed_stages_iid.extend(list(self.view.stagesFrame.tag_has("tristate")))
        allowed_stages = {}
        for stage_iid in allowed_stages_iid:
            stage_item = self.view.stagesFrame.item(stage_iid)
            allowed_stages.setdefault(stage_item["values"][1], stage_item["tags"][0])
        return allowed_stages

    def clear_all(self):
        self.view.stagesFrame.delete(*self.view.stagesFrame.get_children())


    def create_stages_tree(self, zones=data_parser.stages.create_stages_tree(), checked_list=None):
        if checked_list is None:
            checked_list = dict()
        self.view.stagesFrame.delete(*self.view.stagesFrame.get_children())
        for zone in zones:
            zone_iid = self.view.stagesFrame.insert("", tk.END, values=(zones[zone]["name"], zone))
            if zone in checked_list:
                self.view.stagesFrame.change_state(zone_iid, checked_list[zone])
            for stage in zones[zone]:
                if not stage == "name":
                    if zone in ["main_10", "main_11", "main_12"]:
                        stage_iid = self.view.stagesFrame.insert(zone_iid, tk.END, values=(
                            f"{zones[zone][stage]['code']}  {(zones[zone][stage]['diffGroup']).capitalize()}", stage))
                        if stage in checked_list:
                            self.view.stagesFrame.change_state(stage_iid, checked_list[stage])
                    else:
                        stage_iid = self.view.stagesFrame.insert(zone_iid, tk.END, values=(zones[zone][stage]["code"], stage))
                        if stage in checked_list:
                            self.view.stagesFrame.change_state(stage_iid, checked_list[stage])

    def set_binds(self):
        self.view.selectAll.configure(command=lambda: self.select_all())


class StagesFrame:
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.model = Model()
        self.view = View(master=master)
        self.controller = Controller(self.model, self.view)

        self.view.set_controller(self.controller)

        self.controller.create_stages_tree()
        self.controller.set_binds()