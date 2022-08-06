import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import ArknightsDataParser as ADP
import inventoryFrame as iFrame


class CalculateFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.grid(padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.master = master
        self.inventory = ADP.Inventory().inventory
        self.farming_data = {}
        self.inventory_copy = {}
        self.item_list = {}

        self.text = StringVar()
        self.label = tk.Label(self, justify="left", textvariable=self.text)
        self.label.grid(column=0, row=0, sticky="ew")
        self.text.set("Total sanity cost: 0")

        self.bind("<FocusIn>", self.on_visibility)

        self.calculateFrame = ttk.Treeview(self, columns=["name", "need", "cost", "runs", "stage", "itemId"],
                                           displaycolumns=[0, 1, 2, 3, 4, 5])
        self.calculateFrame.grid(column=0, row=1, sticky="nsew")
        self.calculateFrame.column("#0", stretch=False, width=150)
        self.calculateFrame.heading("#0", text="Icon", anchor="center")
        self.calculateFrame.column("name", stretch=True, width=150)
        self.calculateFrame.heading("name", text="Item", anchor="center")
        self.calculateFrame.column("need", stretch=True, width=70)
        self.calculateFrame.heading("need", text="Need", anchor="center")
        self.calculateFrame.column("cost", stretch=True, width=70)
        self.calculateFrame.heading("cost", text="Cost", anchor="center")
        self.calculateFrame.column("runs", stretch=True, width=70)
        self.calculateFrame.heading("runs", text="Runs", anchor="center")
        self.calculateFrame.column("stage", stretch=True, width=150)
        self.calculateFrame.heading("stage", text="Stage", anchor="center")
        self.calculateFrame.column("itemId")
        self.calculateFrame.heading("itemId", text="ItemId")
        self.calculateFrame.tag_configure('comp', background='Yellow')
        self.calculateFrame.tag_configure('farm', background='Red')

        self.create_item_list()

    def create_item_list(self):
        """
        Создает список предметов с иконками для дальнейшей отрисовки таблицы.
        :return: Ничего не возвращает.
        """
        for item in self.inventory.values():
            try:
                icon = Image.open("items/" + item.iconId + ".png")
                icon.thumbnail((20, 20), Image.ANTIALIAS)
                icon = ImageTk.PhotoImage(icon)
                item.icon = icon
            except FileNotFoundError:
                print("File with id " + item.iconId + " not found, skipping...")
                item.icon = None
        return None

    def create_path(self, results):
        """
        Создает дерево результатов с предложениями по крафту и фарму.
        :param results: Принимает на вход список предметов - результаты расчетов. Словарик из id предмета и count
            количества предметов для крафта.
        :return: Ничего не возвращает.
        """
        self.farming_data.clear()  # Чистим farming_data.
        results_copy = results.copy()
        self.inventory_copy = iFrame.InventoryFrame.create_item_list()
        for i in self.calculateFrame.get_children():  # Чистим таблицу.
            self.calculateFrame.delete(i)
        if results_copy:  # Если есть результаты расчетов выполняем строительство дерева.
            for i in results_copy:
                self.create_tree(i, results_copy[i], "")
        self.clear_path(self.item_list)
        self.create_farming_data(self.item_list)
        if self.farming_data:
            self.master.farming.create_path(self.farming_data)  # Вызываем строительство таблицы фарма материалов в другом фрейме.
        return None

    def create_tree(self, itemId, count, last_iid):
        """
        Создает дерево-таблицу предметов и выводит ее в CalculateFrame.calculateFrame.
        :param itemId: ID предмета.
        :param count: Количество предмета.
        :return: Ничего не возвращает.
        """
        item = self.inventory[itemId]
        item.have = iFrame.InventoryFrame.frames[itemId].itemHave.get()
        curr_iid = self.calculateFrame.insert(last_iid, tk.END, image=item.icon,
                                              values=(item.name, count, "", "", "", item.itemId))
        self.calculateFrame.set(curr_iid, column="stage", value=str(curr_iid))
        if item.flags == "Crafting":
            for k in item.formula["costs"]:  # Если присутствует формула - вывести дерево формулы по той же схеме.
                self.create_tree(k["id"], k["count"] * count, curr_iid)
        return None

    def create_children_list(self, item):
        for child in self.calculateFrame.get_children(item):
            item = self.calculateFrame.item(child)
            self.item_list.setdefault(child, {"itemId": str(item.get("values")[5]), "count": item.get("values")[1]})
            if self.calculateFrame.get_children(child).__len__() > 0:
                self.create_children_list(child)

    def clear_path(self, item_list):
        self.item_list.clear()
        self.create_children_list("")
        item_list_copy = item_list.copy()
        for item in item_list_copy:
            itemId = self.item_list[item].get("itemId")
            have = int(self.inventory_copy.get(itemId))
            if have is not None:
                if self.item_list[item].get("count") > have > 0:
                    if self.calculateFrame.exists(item):
                        self.calculateFrame.set(item, column="need", value=self.item_list[item].get("count") - int(self.inventory_copy.get(itemId)))
                        self.inventory_copy[itemId] = 0
                if self.item_list[item].get("count") <= have:
                    self.inventory_copy[itemId] = int(self.inventory_copy.get(itemId)) - self.item_list[item].get("count")
                    self.item_list.pop(item)
                    if self.calculateFrame.exists(item):
                        self.calculateFrame.delete(item)

    def create_farming_data(self, item_list):
        self.item_list.clear()
        self.create_children_list("")
        for item in item_list:
            itemId = self.item_list[item].get("itemId")
            flag = self.inventory.get(itemId).flags
            if flag == "Farming":
                if not self.farming_data.get(itemId):  # Проверка наличия предмета в farming_data.
                    self.farming_data.setdefault(itemId, 0)
                self.farming_data[itemId] += self.item_list[item].get("count")  # Сложение количества предметов внутри farming_data.

    def on_visibility(self, event):
        self.master.planner.calculate()
        self.update()
