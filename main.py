import json
import os
import tkinter as tk
from tkinter import *

import ArknightsDataParser
import inventoryFrame as iFrame
import inventoryPanels
import mainWindow


class EarEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ArknightsDataParser.OperatorState):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Stats):
            return obj.__dict__
        if isinstance(obj, inventoryPanels.InvPanel):
            return obj.__dict__
        if isinstance(obj, iFrame.InventoryFrame):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Operator):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Database):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Item):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Inventory):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def save_data():
    earList = app.planner.allEarsList
    data = {"earList": {}, "inventory": {}, "settings": {}}
    for ears in earList.values():
        data["earList"][ears.name] = {}
        data["earList"][ears.name]["iid"] = ears.iid
        data["earList"][ears.name]["name"] = ears.name
        data["earList"][ears.name]["current"] = ears.current
        data["earList"][ears.name]["desired"] = ears.desired
    for items in iFrame.InventoryFrame.frames.values():
        data["inventory"][items.itemId] = {}
        data["inventory"][items.itemId]["itemId"] = items.itemId
        if items.itemHave.get():
            data["inventory"][items.itemId]["have"] = items.itemHave.get()
    data["settings"]["repository"] = str(app.rep_choose_var.get())
    if os.path.exists("savedata.json"):
        os.remove("savedata.json")
    file = open("savedata.json", 'w+')
    json.dump(data, file, cls=EarEncoder, indent=4)
    file.close()
    root.destroy()


root = tk.Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
app = mainWindow.Application(master=root)
app.restore_data()
root.protocol("WM_DELETE_WINDOW", save_data)
app.mainloop()
