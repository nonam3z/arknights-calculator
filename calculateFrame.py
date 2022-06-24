import math
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
        self.item_list = {}
        self.farming_data = {}
        self.crafting_data = {}

        self.text = StringVar()
        self.label = tk.Label(self, justify="left", textvariable=self.text)
        self.label.grid(column=0, row=0, sticky="ew")
        self.text.set("Total sanity cost: 0")

        self.bind("<Visibility>", self.on_visibility)

        self.calculateFrame = ttk.Treeview(self, columns=["name", "need", "have", "cost", "runs", "stage"])
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
        self.calculateFrame.column("runs", stretch=True, width=70)
        self.calculateFrame.heading("runs", text="Runs", anchor="center")
        self.calculateFrame.column("stage", stretch=True, width=150)
        self.calculateFrame.heading("stage", text="Stage", anchor="center")
        self.calculateFrame.tag_configure('comp', background='Yellow')
        self.calculateFrame.tag_configure('farm', background='Red')

        self.create_item_list()

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

    def create_path(self, results):
        """
        Создает дерево результатов с предложениями по крафту и фарму.
        :param results: Принимает на вход список предметов - результаты расчетов. Словарик из id предмета и count
            количества предметов для крафта.
        :return: Ничего не возвращает.
        """
        self.farming_data.clear()  # Чистим farming_data.
        self.crafting_data.clear()
        for i in self.calculateFrame.get_children():  # Чистим таблицу.
            self.calculateFrame.delete(i)
        if results:  # Если есть результаты расчетов выполняем строительство дерева.
            for i in results:
                self.return_compilated_results(i, results[i], "")
                self.create_tree(i, results[i])
        # !!! Временная функция очистки результатов фарма от того, что уже есть в инвентаре.
        self.farming_data = self.remove_items_from_list(self.farming_data)
        # !!! Останется ли в результате - неизвестно.
        if self.farming_data:
            self.master.farming.create_path(self.farming_data, "")  # Вызываем строительство таблицы фарма материалов в другом фрейме.
        return None

    def remove_items_from_list(self, results):
        """
        Удаляет из списка результатов имеющиеся материалы.
        :return: Ничего не возвращает.
        """
        data = results.copy()
        if results:
            for i in results:
                if results[i] <= int(self.item_list[i].have):
                    data.pop(i)
                if results[i] > int(self.item_list[i].have):
                    data[i] = results[i] - int(self.item_list[i].have)
        return data

    def return_compilated_results(self, itemId, count, curr_iid):
        item = self.item_list[itemId]
        last_iid = self.calculateFrame.insert(curr_iid, tk.END, image=item.icon,
                                              values=(item.name, count, item.have, "", "", ""))
        return last_iid

    def create_tree(self, itemId, count):
        """
        Создает дерево-таблицу предметов и выводит ее в CalculateFrame.calculateFrame.
        :param itemId: ID предмета.
        :param count: Количество предмета.
        :return: Ничего не возвращает.
        """
        item = self.item_list[itemId]
        item.have = iFrame.InventoryFrame.frames[itemId].itemHave.get()
        if item.flags == "Farming":
            if not self.farming_data.get(itemId):  # Проверка наличия предмета в farming_data.
                self.farming_data.setdefault(itemId, 0)
            self.farming_data[itemId] += count  # Сложение количества предметов внутри farming_data.
        if item.flags == "Crafting":
            for k in item.formula["costs"]:  # Если присутствует формула - вывести дерево формулы по той же схеме.
                self.create_tree(k["id"], k["count"] * count)
        return None

    def create_farming_path(self, results, iid):
        """
        Создаем таблицу фарма материалов на основе матрицы stages и данных стоимости материалов.
        :param results: Принимает на вход словарик результатов из id предмета и count количества предмета.
        :param iid: IID родительского элемента в таблице.
        :return: Ничего не возвращает.
        """
        data = ADP.Database()
        stages = data.stages  # Получаем ссылку на матрицу stages.
        total_cost = 0  # Переменная, общая стомость в думалке для фарма.
        ignore = ["5001", "3213", "3223", "3233", "3243", "3253", "3263", "3273", "3283"]  # Игнорим часть предметов.
        if results:
            for item in results:
                if item not in ignore:
                    stage = self.item_list[item].bestStageId
                    runs = math.ceil((self.item_list[item].bestAp * results[item]) / float(
                        stages[stage]["apCost"]))
                    total_cost += runs * stages[stage]["apCost"]
                    self.calculateFrame.insert(iid, tk.END, image=self.item_list[item].icon,
                                               values=(
                                                   self.item_list[item].name, results[item],
                                                   "", stages[stage]["apCost"] * runs,
                                                   runs, self.item_list[item].bestStage))
        self.text.set("Total sanity cost: " + str(total_cost) + ", ETA without Prime: " + str(
            total_cost / 240) + " day(s)" + ", ETA with Prime: " + str(total_cost / 300) + " day(s).")
        return None

    def on_visibility(self, event):
        self.master.planner.calculate()
        self.update()
