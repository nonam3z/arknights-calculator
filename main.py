import mainWindow
import tkinter as tk
from tkinter import *
from urllib.request import urlretrieve


def get_file_from_github(filename):
    repository = "https://raw.githubusercontent.com/Dimbreath/ArknightsData/master/en-US/gamedata/excel/"
    data = (repository+filename+".json")
    file = ("jsons/"+filename+".json")
    urlretrieve(data, file)


def update_script():
    get_file_from_github("character_table")
    get_file_from_github("item_table")
    get_file_from_github("building_data")
    get_file_from_github("gamedata_const")
    get_file_from_github("stage_table")


update_script()


root = tk.Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
app = mainWindow.Application(master=root)
root.protocol("WM_DELETE_WINDOW", root.destroy)
app.mainloop()
