import re
import tkinter as tk
from tkinter import ttk

import ttkwidgets as ttkw

import ArknightsDataParser as ADP


class StagesFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.stages = ADP.Database().stages

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
        zones = {}
        for stage in self.stages.values():
            if not zones.get(stage["zoneId"]):
                zones.setdefault(stage["zoneId"], {})
        pattern = r"(main).*|(weekly).*"
        zones2 = zones.copy()
        for zone in zones2:
            if not re.fullmatch(pattern, zone):
                zones.pop(zone)
        for stage in self.stages.values():
            if stage["zoneId"] in zones:
                if not zones[stage["zoneId"]].get(stage["stageId"]):
                    stagespattern = r".*(#f#)|(tr).*"
                    if not re.fullmatch(stagespattern, stage["stageId"]):
                        zones[stage["zoneId"]].setdefault(stage["stageId"], stage)
        for zone in zones:
            zone_iid = self.stagesFrame.insert("", tk.END, values=(zone, zone))
            if zone in checked_list:
                self.stagesFrame.change_state(zone_iid, checked_list[zone])
            for stage in zones[zone]:
                stage_iid = self.stagesFrame.insert(zone_iid, tk.END, values=(zones[zone][stage]["code"], stage))
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
