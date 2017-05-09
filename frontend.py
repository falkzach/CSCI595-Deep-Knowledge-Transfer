#!/usr/bin/env python

import tkinter as tk
import tkinter.filedialog as fd


class Frontend(tk.Frame):

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.app = app

        self.file_path = tk.StringVar()

        self.initUI()

    def initUI(self):
        # Test buttons for initial tinkering
        tk.Label(self, text="Test Buttons").place(x=0, y = 475)
        tk.Button(self, text="Test", command=self.test).place(x=75, y=475)
        tk.Button(self, text="CNN MNIST", command=self.cnn_mst).place(x=125, y=475)
        tk.Button(self, text="Hello", command=self.hello).place(x=225, y=475)

        job_queue_lstbox = tk.Listbox(self)
        job_queue_lstbox.place(x=25, y=0)
        job_queue_lstbox.insert(tk.END, "No Jobs Queued")

        current_job_label = tk.Label(self, text="Current Job: None")
        current_job_label.place(x=25, y=190)

        finished_jobs_lstbox = tk.Listbox(self)
        finished_jobs_lstbox.place(x=25, y=225)
        finished_jobs_lstbox.insert(tk.END, "No Jobs Finished")

        file_path_text = tk.Entry(self, width=75, textvariable=self.file_path)
        file_path_text.place(x=200, y=25)

        load_job_button = tk.Button(self, text="Load", command= lambda: self.load_file(file_path_text))
        load_job_button.place(x=200, y=0)

        queue_job_button = tk.Button(self, text="Queue", command=lambda: self.queue())
        queue_job_button.place(x=275, y=0)



        self.pack(fill=tk.BOTH, expand=1)

    def test(self):
        self.app.test_job()

    def cnn_mst(self):
        self.app.test_cnn_mnst()

    def hello(self):
        self.app.test_hello()

    def load_file(self, display):
        path = fd.askopenfilename(
            filetypes=( ("Python Tensor FLow File", "*.py"), ),
        )
        self.file_path.set(path)

    def queue(self):
        path = self.file_path.get()
        self.app.queue_by_path(path)
        self.file_path.set("")
