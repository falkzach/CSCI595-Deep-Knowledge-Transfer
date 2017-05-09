#!/usr/bin/env python

import tkinter as tk
import tkinter.filedialog as fd


class Frontend(tk.Frame):

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.app = app
        self.output_pane = None

        self.file_path = tk.StringVar()
        self.current_job = tk.StringVar()

        self.initUI()

    def initUI(self):
        # Test buttons for initial tinkering
        tk.Label(self, text="Test Buttons").place(x=0, y = 675)
        tk.Button(self, text="Test", command=self.test).place(x=75, y=675)
        tk.Button(self, text="CNN MNIST", command=self.cnn_mst).place(x=125, y=675)
        tk.Button(self, text="Hello", command=self.hello).place(x=225, y=675)

        self.job_queue_lstbox = tk.Listbox(self)
        self.job_queue_lstbox.place(x=25, y=0)
        self.job_queue_lstbox.insert(tk.END, "No Jobs Queued")

        self.current_job_label = tk.Label(self, textvariable=self.current_job)
        self.current_job_label.place(x=25, y=190)

        self.finished_jobs_lstbox = tk.Listbox(self)
        self.finished_jobs_lstbox.place(x=25, y=225)

        self.file_path_text = tk.Entry(self, width=75, textvariable=self.file_path)
        self.file_path_text.place(x=200, y=25)

        self.load_job_button = tk.Button(self, text="Load", command= lambda: self.load_file(self.file_path.get()))
        self.load_job_button.place(x=200, y=0)

        self.queue_job_button = tk.Button(self, text="Queue", command=lambda: self.queue())
        self.queue_job_button.place(x=275, y=0)

        self.output_pane = tk.Text(self, wrap = 'word')
        self.output_pane.place(x=200, y=50)

        self.pack(fill=tk.BOTH, expand=1)

    def test(self):
        self.app.test_job()

    def cnn_mst(self):
        self.app.test_cnn_mnst()

    def hello(self):
        self.app.test_hello()
        self.call_update()

    def load_file(self, display):
        path = fd.askopenfilename(
            filetypes=( ("Python Tensor FLow File", "*.py"), ),
        )
        self.file_path.set(path)

    def queue(self):
        path = self.file_path.get()
        self.app.queue_by_path(path)
        self.file_path.set("")

    def get_output_pane(self):
        return self.output_pane

    def update_elements(self):
        self.current_job.set(self.app.job) # TODO: make a job object, store the name?

        # front = self.finished_jobs_lstbox.size()
        # back = len(self.app.finished_jobs)
        # if (back > front):
        #     for i in range(back,front):
        #         self.finished_jobs_lstbox.insert(tk.END, self.app.finished_jobs[back])

        self.call_update()

    def call_update(self):
        self.app.root.after(1000, self.update_elements)

