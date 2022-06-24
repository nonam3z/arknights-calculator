import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import ArknightsDataParser as ADP


class ItemDataFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.item_list = {}
        self.farming_data = {}
        self.crafting_data = {}

        self.text = StringVar()
        self.label = tk.Label(self, justify="left", textvariable=self.text)
        self.label.grid(column=0, row=0, sticky="ew")
        self.text.set("Filler Label")

        self.itemData = ttk.Treeview(self, columns=["name", "cost", "ccost", "flags"])
        self.itemData.grid(column=0, row=1, sticky="nsew")
        self.itemData.column("#0", stretch=False, width=150)
        self.itemData.heading("#0", text="Icon", anchor="center")
        self.itemData.column("name", stretch=True, width=150)
        self.itemData.heading("name", text="Item", anchor="center")
        self.itemData.column("cost", stretch=True, width=70)
        self.itemData.heading("cost", text="AP Cost", anchor="center")
        self.itemData.column("ccost", stretch=True, width=70)
        self.itemData.heading("ccost", text="Craft Cost", anchor="center")
        self.itemData.column("flags", stretch=True, width=70)
        self.itemData.heading("flags", text="Flags", anchor="center")

        self.create_item_list()
        self.create_info()

    def create_item_list(self):
        """
        Создает список предметов с иконками для дальнейшей отрисовки таблицы.
        :return: Ничего не возвращает.
        """
        self.item_list = ADP.Inventory().inventory
        for item in self.item_list.values():
            try:
                icon = Image.open("items/" + item.iconId + ".png")
                icon.thumbnail((20, 20), Image.ANTIALIAS)
                icon = ImageTk.PhotoImage(icon)
                item.icon = icon
            except FileNotFoundError:
                print("File with id " + item.iconId + " not found, skipping...")
                item.icon = None
        return None

    def create_info(self):
        for item in self.item_list.values():
            self.itemData.insert("", tk.END, image=item.icon,
                                 values=(item.name, item.bestAp, item.craftingAp, item.flags))
