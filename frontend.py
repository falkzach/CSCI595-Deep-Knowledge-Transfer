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
        self.current_experiment = tk.StringVar()

        # Test buttons for initial tinkering
        tk.Label(self, text="Test Buttons").place(x=0, y = 675)
        tk.Button(self, text="CNN MNIST", command=self.cnn_mst).place(x=75, y=675)
        tk.Button(self, text="Hello", command=self.hello).place(x=150, y=675)

        self.queued_experiments_label = tk.Label(self, text="Queued Experiments")
        self.queued_experiments_label.place(x=25, y=25)
        self.experiment_queue_listbox = tk.Listbox(self, width=40)
        self.experiment_queue_listbox.place(x=25, y=50)

        self.finished_experiments_label = tk.Label(self, text="Finished Experiments")
        self.finished_experiments_label.place(x=25, y=275)
        self.finished_experiments_listbox = tk.Listbox(self, width=40)
        self.finished_experiments_listbox.place(x=25, y=300)

        self.file_path_text = tk.Entry(self, width=75, textvariable=self.file_path)
        self.file_path_text.place(x=300, y=25)

        self.load_experiments_button = tk.Button(self, text="Load", command= lambda: self.load_file(self.file_path.get()))
        self.load_experiments_button.place(x=300, y=0)

        self.queue_experiment_button = tk.Button(self, text="Queue", command=lambda: self.queue())
        self.queue_experiment_button.place(x=375, y=0)

        self.label_current_experiment = tk.Label(self, text="Current Experiment")
        self.label_current_experiment.place(x=300, y=50)

        self.current_experiment_label = tk.Label(self, textvariable=self.current_experiment)
        self.current_experiment_label.place(x=425, y=50)

        self.output_pane = tk.Text(self, wrap = 'none')
        self.output_pane.place(x=300, y=75)

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
        self.experiment_queue_listbox.delete(0, tk.END)
        for experiment in list(self.app.experiment_queue.queue):
            self.experiment_queue_listbox.insert(tk.END, experiment.name)

        # Current experiment
        current_experiment = "None"
        if self.app.tf_thread is not None:
            current_experiment = self.app.tf_thread.name
        self.current_experiment.set(current_experiment)

        # Finished experiments, find unaccounted for and populate
        front = self.finished_experiments_listbox.size()
        back = len(self.app.finished_experiments)
        if back > front:
            for i in range(front, back):
                self.finished_experiments_listbox.insert(tk.END, self.app.finished_experiments[back - 1].name)

        self.call_update()

    def call_update(self):
        self.app.root.after(1000, self.update_elements)

