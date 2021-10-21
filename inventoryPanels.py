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

        self.itemIcon = tk.Canvas(self, width=50, height=50)
        self.itemIcon.grid(row=1, column=0, sticky="nsew")

        self.itemName = tk.Label(self, width=180)
        self.itemName.grid(row=0, column=0, columnspan=2)

        self.itemHave = ttk.Spinbox(self, from_=0, to=999999999)
        self.itemHave.grid(row=1, column=1)

        # self.itemNeed = ttk.Spinbox(self)
        # self.itemNeed.grid(row=2, column=1)


None
