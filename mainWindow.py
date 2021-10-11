import tkinter as tk
from tkinter import ttk
import plannerFrame
import inventoryFrame
import PictureTest


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Arknights Calculator")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        master.minsize(width=1200, height=900)
        master.maxsize(width=1200, height=900)
        master.resizable(width=True, height=True)
        self.grid(padx=5, pady=5, sticky="nsew")

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(plannerFrame.Planner(self), text="Planner")
        self.tabs.add(inventoryFrame.InventoryFrame(self), text="Inventory Depot")
        self.tabs.add(PictureTest.PictureTest(self), text="Testing Facility")

