import mainWindow
import os
import tkinter as tk
from tkinter import *
import json
import ArknightsDataParser


class EarEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ArknightsDataParser.OperatorState):
            return obj.__dict__
        if isinstance(obj, ArknightsDataParser.Stats):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def save_list():
    earList = app.planner.allEarsList
    if os.path.exists("savedata.json"):
        os.remove("savedata.json")
    file = open("savedata.json", 'w+')
    json.dump(earList, file, cls=EarEncoder)
    file.close()
    root.destroy()


root = tk.Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
app = mainWindow.Application(master=root)
app.restore_data()
root.protocol("WM_DELETE_WINDOW", save_list)
app.mainloop()
