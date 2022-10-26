# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import tkinter as tk
from tkinter import ttk


class InvPanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)

        self.itemId = ""
        self.iconId = ""
        self.icon = ""
        # self.thumbnail = ""

        self.vcmdInv = (self.register(self.validateInv), "%P", "%W")
        self.ivcmd = (self.register(self.onInvalid), "%W", "%P")

        self.itemIcon = tk.Canvas(self, width=50, height=50)
        self.itemIcon.grid(row=1, column=0, sticky="nsew")

        self.itemName = tk.Label(self, width=180)
        self.itemName.grid(row=0, column=0, columnspan=2)

        self.itemHave = ttk.Spinbox(self, from_=0, to=999999999)
        self.itemHave.grid(row=1, column=1)
        self.itemHave.configure(validate="key", validatecommand=self.vcmdInv, invalidcommand=self.ivcmd)

    def validateInv(self, P, W):
        widget = self.master.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        try:
            if P == "":
                return True
            if P.isdigit():
                if _from <= int(P) <= _to:
                    return True
        except ValueError:
            return False
        return False

    def onInvalid(self, W, P):
        widget = self.master.nametowidget(W)
        _from = widget["from"]
        _to = widget["to"]
        widget.delete(0, 99)
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

