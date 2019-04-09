# -*- coding: utf-8 -*-

import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        self.super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
