import tkinter as tk
from tkinter import ttk
from tkinter import *

import inventoryFrame as iFrame
import plannerFrame
import plannerPanels
import ArknightsDataParser as ADP
import win32clipboard
import json
import math
from PIL import Image, ImageTk


class CalculateFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.item_list = {}

        self.button = tk.Button(self, text="Calculate Path", command=self.create_path)
        self.button.grid(column=0, row=0, sticky="ew")

        self.calculateFrame = ttk.Treeview(self, columns=["name", "need", "have", "cost", "stage"])
        self.calculateFrame.grid(column=0, row=1, sticky="nsew")
        self.calculateFrame.column("#0", stretch=False, width=150)
        self.calculateFrame.heading("#0", text="Icon", anchor="center")
        self.calculateFrame.column("name", stretch=True, width=150)
        self.calculateFrame.heading("name", text="Item", anchor="center")
        self.calculateFrame.column("need", stretch=True, width=70)
        self.calculateFrame.heading("need", text="Need", anchor="center")
        self.calculateFrame.column("have", stretch=True, width=70)
        self.calculateFrame.heading("have", text="Have", anchor="center")
        self.calculateFrame.column("cost", stretch=True, width=70)
        self.calculateFrame.heading("cost", text="Cost", anchor="center")
        self.calculateFrame.column("stage", stretch=True, width=150)
        self.calculateFrame.heading("stage", text="Stage", anchor="center")

        self.create_item_list()
        self.create_path()

    def create_item_list(self):
        self.item_list = ADP.inventory.items
        for item in self.item_list.values():
            icon = Image.open("items/" + item.iconId + ".png")
            icon.thumbnail((20, 20), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(icon)
            item.icon = icon
            item.have = iFrame.InventoryFrame.frames[item.itemId].itemHave.get()
        return None

    def create_path(self):
        results = plannerFrame.Planner.results
        for i in self.calculateFrame.get_children():
            self.calculateFrame.delete(i)
        if results:
            for i in results:
                self.create_tree(i, results[i], "i000")

                # if self.item_list[i].flags == "Farming":
                #     self.calculateFrame.insert("", tk.END, iid=i, image=self.item_list[i].icon,
                #                                values=(self.item_list[i].name, results[i], self.item_list[i].have,
                #                                        self.item_list[i].bestAp * results[i], self.item_list[i].bestStage))
                # if self.item_list[i].flags == "Crafting":
                #     self.calculateFrame.insert("", tk.END, iid=i, image=self.item_list[i].icon,
                #                                values=(self.item_list[i].name, results[i], self.item_list[i].have,
                #                                        "Crafting", "Workshop"))
                #     for k in self.item_list[i].formula["costs"]:
                #         self.calculateFrame.insert(parent=i, index=tk.END, image=self.item_list[k["id"]].icon,
                #                                    values=(self.item_list[k["id"]].name, (results[i]) * k["count"],
                #                                     self.item_list[k["id"]].have, self.item_list[k["id"]].bestAp * k["count"],
                #                                     self.item_list[k["id"]].bestStage))

    def create_tree(self, item, count, curr_iid):
        if curr_iid == "i000":
            if self.item_list[item].flags == "Farming":
                last_iid = self.calculateFrame.insert("", tk.END, image=self.item_list[item].icon,
                                                      values=(
                                                          self.item_list[item].name, count, self.item_list[item].have,
                                                          self.item_list[item].bestAp * count,
                                                          self.item_list[item].bestStage))
            if self.item_list[item].flags == "Crafting":
                last_iid = self.calculateFrame.insert("", tk.END, image=self.item_list[item].icon,
                                                      values=(
                                                          self.item_list[item].name, count, self.item_list[item].have,
                                                          "Crafting", "Workshop"))
                for k in self.item_list[item].formula["costs"]:
                    if self.item_list[k["id"]].flags == "Farming":
                        child_iid = self.calculateFrame.insert(parent=last_iid, index=tk.END,
                                                               image=self.item_list[k["id"]].icon,
                                                               values=(self.item_list[k["id"]].name, count * k["count"],
                                                                       self.item_list[k["id"]].have,
                                                                       self.item_list[k["id"]].bestAp * k["count"],
                                                                       self.item_list[k["id"]].bestStage))
                    if self.item_list[k["id"]].flags == "Crafting":
                        self.create_tree(k["id"], k["count"] * count, last_iid)
        else:
            if self.item_list[item].flags == "Farming":
                last_iid = self.calculateFrame.insert(parent=curr_iid, index=tk.END, image=self.item_list[item].icon,
                                                      values=(
                                                          self.item_list[item].name, count, self.item_list[item].have,
                                                          self.item_list[item].bestAp * count,
                                                          self.item_list[item].bestStage))
            if self.item_list[item].flags == "Crafting":
                last_iid = self.calculateFrame.insert(parent=curr_iid, index=tk.END, image=self.item_list[item].icon,
                                                      values=(
                                                          self.item_list[item].name, count, self.item_list[item].have,
                                                          "Crafting", "Workshop"))
                for k in self.item_list[item].formula["costs"]:
                    if self.item_list[k["id"]].flags == "Farming":
                        child_iid = self.calculateFrame.insert(parent=last_iid, index=tk.END,
                                                               image=self.item_list[k["id"]].icon,
                                                               values=(self.item_list[k["id"]].name, count * k["count"],
                                                                       self.item_list[k["id"]].have,
                                                                       self.item_list[k["id"]].bestAp * k["count"],
                                                                       self.item_list[k["id"]].bestStage))
                    if self.item_list[k["id"]].flags == "Crafting":
                        self.create_tree(k["id"], k["count"] * count, last_iid)
