import math
import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import ArknightsDataParser as ADP
import inventoryFrame as iFrame


class FarmingFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.item_list = {}
        self.farming_list = {}

        self.text = StringVar()
        self.label = tk.Label(self, justify="left", textvariable=self.text)
        self.label.grid(column=0, row=0, sticky="ew")
        self.text.set("Total sanity cost: 0")

        self.farmingFrame = ttk.Treeview(self, columns=["name", "need", "have", "cost", "stage", "runs", "sanity"])
        self.farmingFrame.grid(column=0, row=1, sticky="nsew")
        self.farmingFrame.column("#0", stretch=False, width=150)
        self.farmingFrame.heading("#0", text="Icon", anchor="center")
        self.farmingFrame.column("name", stretch=True, width=150)
        self.farmingFrame.heading("name", text="Item", anchor="center")
        self.farmingFrame.column("need", stretch=True, width=50)
        self.farmingFrame.heading("need", text="Need", anchor="center")
        self.farmingFrame.column("have", stretch=True, width=50)
        self.farmingFrame.heading("have", text="Have", anchor="center")
        self.farmingFrame.column("cost", stretch=True, width=150)
        self.farmingFrame.heading("cost", text="Ap per item", anchor="center")
        self.farmingFrame.column("stage", stretch=True, width=50)
        self.farmingFrame.heading("stage", text="Stage", anchor="center")
        self.farmingFrame.column("runs", stretch=True, width=50)
        self.farmingFrame.heading("runs", text="Runs", anchor="center")
        self.farmingFrame.column("sanity", stretch=True, width=50)
        self.farmingFrame.heading("sanity", text="Sanity", anchor="center")

        self.create_item_list()

    def create_item_list(self):
        """
        Создает список предметов с иконками для дальнейшей отрисовки таблицы.
        :return: Ничего не возвращает.
        """
        self.item_list = ADP.inventory.items
        for item in self.item_list.values():
            icon = Image.open("items/" + item.iconId + ".png")
            icon.thumbnail((20, 20), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(icon)
            item.icon = icon
            item.have = iFrame.InventoryFrame.frames[item.itemId].itemHave.get()
        return None

    def create_path(self, results):
        """
        Создаем таблицу фарма материалов на основе матрицы stages и данных стоимости материалов.
        :param results: Принимает на вход словарик результатов из id предмета и count количества предмета.
        :return: Ничего не возвращает.
        """
        stages = ADP.stages     # Получаем ссылку на матрицу stages.
        total_cost = 0      # Переменная, общая стомость в думалке для фарма.
        ignore = ["5001", "3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283"]   # Игнорим часть предметов.
        for i in self.farmingFrame.get_children():  # Чистим таблицу.
            self.farmingFrame.delete(i)
        if results:
            for item in results:
                if item not in ignore:
                    have = iFrame.InventoryFrame.frames[item].itemHave.get()
                    stage = self.item_list[item].bestStageId
                    if int(have) < results[item]:
                        runs = math.ceil((self.item_list[item].bestAp * (results[item] - float(have))/float(stages[stage]["apCost"])))
                    else:
                        runs = 0
                    total_cost += runs * stages[stage]["apCost"]
                    if runs != 0:
                        self.farmingFrame.insert("", tk.END, image=self.item_list[item].icon,
                                                 values=(
                                                   self.item_list[item].name, results[item],
                                                   have,
                                                   self.item_list[item].bestAp,
                                                   self.item_list[item].bestStage,
                                                   runs,
                                                   stages[stage]["apCost"] * runs))
        self.text.set("Total sanity cost: "+str(total_cost)+", ETA without Prime: "+str(total_cost/240)+", ETA with Prime: "+str(total_cost/300))
        return None
