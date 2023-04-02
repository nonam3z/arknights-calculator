# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import re
import tkinter as tk
from tkinter import ttk

import ttkwidgets as ttkw

from data_parser.database import Database


class StagesFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.stages = Database().stages
        self.zones = Database().zones

        self.selectAll = ttk.Button(self, text="Select All", command=lambda: self.select_all())
        self.selectAll.grid(column=0, row=0)

        self.stagesFrame = ttkw.CheckboxTreeview(self, columns=["name", "stageId"])
        self.stagesFrame.grid(column=0, row=1, sticky="nsew")
        self.stagesFrame.column("#0", stretch=False, width=150)
        self.stagesFrame.heading("#0", text="Icon", anchor="center")
        self.stagesFrame.column("name", stretch=True, width=150)
        self.stagesFrame.heading("name", text="Name", anchor="center")
        self.stagesFrame.column("stageId", stretch=True, width=150)
        self.stagesFrame.heading("stageId", text="Stage Id", anchor="center")

        self.create_visible_tree({})

    def select_all(self):
        for iid in self.stagesFrame.get_children():
            self.stagesFrame.change_state(iid, "checked")
            for child_iid in self.stagesFrame.get_children(iid):
                self.stagesFrame.change_state(child_iid, "checked")

    def create_visible_tree(self, checked_list):
        self.stagesFrame.delete(*self.stagesFrame.get_children())
        _zones = {}
        for stage in self.stages.values():
            if not _zones.get(stage["zoneId"]):
                _zones.setdefault(stage["zoneId"], {})
        pattern = r"(main).*|(weekly).*"
        zones2 = _zones.copy()
        for zone in zones2:
            if not re.fullmatch(pattern, zone):
                _zones.pop(zone)
        for stage in self.stages.values():
            if stage["zoneId"] in _zones:
                if not _zones[stage["zoneId"]].get(stage["stageId"]):
                    stagespattern = r".*(#f#)|(tr).*"
                    if not re.fullmatch(stagespattern, stage["stageId"]):
                        _zones[stage["zoneId"]].setdefault(stage["stageId"], stage)
        for zone in _zones:
            if self.zones[zone].get("zoneNameFirst"):
                zone_name = self.zones[zone].get("zoneNameFirst")
            else:
                zone_name = self.zones[zone].get("zoneNameSecond")
            zone_iid = self.stagesFrame.insert("", tk.END, values=(zone_name, zone))
            if zone in checked_list:
                self.stagesFrame.change_state(zone_iid, checked_list[zone])
            for stage in _zones[zone]:
                stage_iid = self.stagesFrame.insert(zone_iid, tk.END, values=(_zones[zone][stage]["code"], stage))
                if stage in checked_list:
                    self.stagesFrame.change_state(stage_iid, checked_list[stage])
        pass

    def create_checked_list(self):
        allowed_stages_iid = list(self.stagesFrame.tag_has("checked"))
        allowed_stages_iid.extend(list(self.stagesFrame.tag_has("tristate")))
        allowed_stages = {}
        for stage_iid in allowed_stages_iid:
            stage_item = self.stagesFrame.item(stage_iid)
            allowed_stages.setdefault(stage_item["values"][1], stage_item["tags"][0])
        return allowed_stages

    def clear_all(self):
        self.stagesFrame.delete(*self.stagesFrame.get_children())
