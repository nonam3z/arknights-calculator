import tkinter as tk
from tkinter import ttk
from tkinter import *
import ArknightsDataParser
import inventoryPanels
import math
from PIL import Image, ImageTk



inv = inventoryPanels.create_inventory()
inventoryPanels.calc_cost(inv)

i = int(inv.__len__())
j = math.ceil(i/6)


class InventoryFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(padx=5, pady=5, sticky="nsew")
        self.master = master

        for c in range(6):
            self.columnconfigure(c, weight=1)
            for r in range(j):
                self.rowconfigure(r, weight=1)

        self.frames = []

        for i in inv.values():
            item = inventoryPanels.InvPanel(self)
            item.itemId = i["itemId"]
            item.itemName.configure(text=i["name"], justify="right", anchor="e")
            item.itemHave.insert(0, "0")
            item.coos = Image.open("items/"+i["iconId"]+".png")
            item.coos.thumbnail((40, 40), Image.ANTIALIAS)
            item.imgIcon = ImageTk.PhotoImage(item.coos)
            item.itemIcon.create_image(10, 5, anchor="nw", image=item.imgIcon)
            self.frames.append(item)

        l = 0
        for n in range(j):
            for m in range(6):
                if l<self.frames.__len__():
                    self.frames[l].grid(row=n, column=m, sticky="nsew")
                    l += 1
                else: break

        for a in range(self.frames.__len__()):
            self.show_frame(a)

    def show_frame(self, index):
        frame = self.frames[index]
        frame.tkraise()