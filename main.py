import mainWindow
import os
import tkinter as tk
from tkinter import *
import json
import ArknightsDataParser
import inventoryPanels
import inventoryFrame

savedata = {}


class EarEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ArknightsDataParser.OperatorState):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Stats):
            return obj.__dict__
        if isinstance(obj, inventoryPanels.InvPanel):
            return obj.__dict__
        if isinstance(obj, inventoryFrame.InventoryFrame):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def save_list():
    savedata["earList"] = app.planner.allEarsList
    savedata["inventory"] = {}
    for items in inventoryFrame.frames.values():
        savedata["inventory"][items.itemId] = {}
        savedata["inventory"][items.itemId]["itemId"] = items.itemId
        savedata["inventory"][items.itemId]["have"] = items.itemHave.get()
    if os.path.exists("savedata.json"):
        os.remove("savedata.json")
    file = open("savedata.json", 'w+')
    json.dump(savedata, file, cls=EarEncoder)
    file.close()
    root.destroy()


root = tk.Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
app = mainWindow.Application(master=root)
app.restore_data()
root.protocol("WM_DELETE_WINDOW", save_list)
app.mainloop()
