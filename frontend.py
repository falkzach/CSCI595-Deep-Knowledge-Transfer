#!/usr/bin/env python

import tkinter as tk
import tkinter.filedialog as fd


class Frontend(tk.Frame):

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.app = app

        self.configure(background='grey')

        self.file_path = tk.StringVar()
        self.current_job = tk.StringVar()

        # Test buttons for initial tinkering
        tk.Label(self, text="Test Buttons").place(x=0, y = 675)
        tk.Button(self, text="CNN MNIST", command=self.cnn_mst).place(x=75, y=675)
        tk.Button(self, text="Hello", command=self.hello).place(x=150, y=675)

        self.job_queue_label = tk.Label(self, text="Queued Jobs")
        self.job_queue_label.place(x=25, y=25)
        self.job_queue_lstbox = tk.Listbox(self, width=40)
        self.job_queue_lstbox.place(x=25, y=50)

        self.finished_queue_label = tk.Label(self, text="Finished Jobs")
        self.finished_queue_label.place(x=25, y=275)
        self.finished_jobs_lstbox = tk.Listbox(self, width=40)
        self.finished_jobs_lstbox.place(x=25, y=300)

        self.file_path_text = tk.Entry(self, width=75, textvariable=self.file_path)
        self.file_path_text.place(x=300, y=25)

        self.load_job_button = tk.Button(self, text="Load", command= lambda: self.load_file(self.file_path.get()))
        self.load_job_button.place(x=300, y=0)

        self.queue_job_button = tk.Button(self, text="Queue", command=lambda: self.queue())
        self.queue_job_button.place(x=375, y=0)

        self.current_job_label = tk.Label(self, textvariable=self.current_job)
        self.current_job_label.place(x=300, y=50)

        self.output_pane = tk.Text(self, wrap = 'none')
        self.output_pane.place(x=300, y=100)

        self.pack(fill=tk.BOTH, expand=1)

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
        # Queued Jobs, clear and re populate
        self.job_queue_lstbox.delete(0, tk.END)
        for job in list(self.app.job_queue.queue):
            self.job_queue_lstbox.insert(tk.END, job)

        # Current Job, set to current job
        self.current_job.set(self.app.job)  # TODO: make a job object, store the name?

        # Finished Jobs, find unaccounted for and populate
        front = self.finished_jobs_lstbox.size()
        back = len(self.app.finished_jobs)
        if (back > front):
            for i in range(front, back):
                self.finished_jobs_lstbox.insert(tk.END, self.app.finished_jobs[back-1])

        self.call_update()

    def call_update(self):
        self.app.root.after(1000, self.update_elements)

