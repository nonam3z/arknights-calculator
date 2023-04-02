# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import re
import tkinter as tk
from tkinter import ttk


class ModulesPanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.columnconfigure(1, weight=1)

        self.ear = ""
        self.master = master

        tk.Label(self, justify="left", text="Module X", width=9).grid(column=0, row=0)
        tk.Label(self, justify="left", text="Module Y", width=9).grid(column=0, row=1)

        self.vcmd = (self.register(self.validate))
        self.ivcmd = (self.register(self.onInvalid))

        self.module_x = ttk.Spinbox(self, from_=0, to=3)
        self.module_x.insert(0, "0")
        self.module_x.configure(validate="all", validatecommand=(self.vcmd, "%P", "W", str(""r"\d")), invalidcommand=self.ivcmd)
        self.module_x.grid(column=1, row=0, sticky="ew")

        self.module_y = ttk.Spinbox(self, from_=0, to=3)
        self.module_y.insert(0, "0")
        self.module_y.configure(validate="all", validatecommand=(self.vcmd, "%P", "W", str(""r"\d")), invalidcommand=self.ivcmd)
        self.module_y.grid(column=1, row=1, sticky="ew")

    def validate(self, P, W, pattern):
        widget = self.master.nametowidget(W)
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

