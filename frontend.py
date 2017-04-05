#!/usr/bin/env python

import tkinter as tk

class Frontend(tk.Frame):

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.main = main

        self.initUI()

    def initUI(self):
        quitButton = tk.Button(self, text="Test", command=self.testTF).place(x=50, y=50)

        self.pack(fill=tk.BOTH, expand=1)

    def testTF(self):
        self.main.test_job()
