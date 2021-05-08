import mainWindow
import tkinter as tk
from tkinter import *
# from urllib.request import urlretrieve

# def update_database(filename): # just updating data
#     repository = "https://raw.githubusercontent.com/Dimbreath/ArknightsData/master/en-US/gamedata/excel/"
#     data = (repository+filename+".json")
#     file = ("jsons/"+filename+".json")
#     urlretrieve(data, file)
#
#
# update_database("character_table")
# update_database("item_table")
# update_database("building_data")
# update_database("gamedata_const")

root = tk.Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
app = mainWindow.Application(master=root)
root.protocol("WM_DELETE_WINDOW", root.destroy)
app.mainloop()
