import re
import tkinter as tk

import ttkwidgets as ttkw

import ArknightsDataParser as ADP


class StagesFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.master = master
        self.stages = ADP.Database().stages

        self.stagesFrame = ttkw.CheckboxTreeview(self, columns=["name", "stageId"])
        self.stagesFrame.grid(column=0, row=0, sticky="nsew")
        self.stagesFrame.column("#0", stretch=False, width=150)
        self.stagesFrame.heading("#0", text="Icon", anchor="center")
        self.stagesFrame.column("name", stretch=True, width=150)
        self.stagesFrame.heading("name", text="Name", anchor="center")
        self.stagesFrame.column("stageId", stretch=True, width=150)
        self.stagesFrame.heading("stageId", text="Stage Id", anchor="center")

        self.create_visible_tree()

    def create_visible_tree(self):
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
            lastIid = self.stagesFrame.insert("", tk.END, values=(zone, ""))
            for stage in zones[zone]:
                self.stagesFrame.insert(lastIid, tk.END, values=(zones[zone][stage]["code"], stage))
        pass
