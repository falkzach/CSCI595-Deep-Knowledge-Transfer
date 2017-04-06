#!/usr/bin/env python

import tkinter as tk


class Frontend(tk.Frame):

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.main = main

        self.initUI()

    def initUI(self):
        tk.Button(self, text="Test", command=self.test).place(x=50, y=50)
        tk.Button(self, text="CNN MNIST", command=self.cnn_mst).place(x=100, y=50)
        tk.Button(self, text="Hello", command=self.hello).place(x=200, y=50)

        self.pack(fill=tk.BOTH, expand=1)

    def test(self):
        self.main.test_job()

    def cnn_mst(self):
        self.main.test_cnn_mnst()

    def hello(self):
        print("Hello!")
