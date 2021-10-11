import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


class PictureTest(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)

        self.image = tk.Canvas(self, width = 300, height = 300)
        self.image.pack()
        self.imgPath = PhotoImage(file="items/MTL_SL_STRG1.png")
        self.image.create_image(10, 10, anchor="nw", image=self.imgPath)

