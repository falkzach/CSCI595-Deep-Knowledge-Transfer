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
        self.current_experiment.set("None")

        # Test buttons for initial tinkering
        tk.Label(self, text="Test Buttons").place(x=0, y=675)
        tk.Button(self, text="CNN MNIST", command=self.cnn_mst).place(x=75, y=675)
        tk.Button(self, text="Hello", command=self.hello).place(x=150, y=675)

        # First Column
        self.queued_experiments_label = tk.Label(self, text="Queued Experiments:")
        self.queued_experiments_label.place(x=25, y=25)
        self.experiment_queue_listbox = tk.Listbox(self, width=40)
        self.experiment_queue_listbox.place(x=25, y=50)

        self.finished_experiments_label = tk.Label(self, text="Finished Experiments:")
        self.finished_experiments_label.place(x=25, y=225)
        self.finished_experiments_listbox = tk.Listbox(self, width=40)
        self.finished_experiments_listbox.place(x=25, y=250)

        self.loaded_experiments_label = tk.Label(self, text="Loaded Experiments:")
        self.loaded_experiments_label.place(x=25, y=425)
        self.loaded_experiments_listbox = tk.Listbox(self, width=40)
        self.loaded_experiments_listbox.place(x=25, y=450)

        # Second Column
        self.file_path_text = tk.Entry(self, width=75, textvariable=self.file_path)
        self.file_path_text.place(x=300, y=25)

        self.open_file_button = tk.Button(self, text="Open",
                                          command=lambda: self.open_file())
        self.open_file_button.place(x=300, y=0)

        self.queue_experiment_button = tk.Button(self, text="Queue", command=lambda: self.queue())
        self.queue_experiment_button.place(x=375, y=0)

        self.load_checkpoint_button = tk.Button(self, text="Load Checkpoint", command=lambda: self.load_experiment())
        self.load_checkpoint_button.place(x=425, y=0)

        self.label_current_experiment = tk.Label(self, text="Current Experiment:")
        self.label_current_experiment.place(x=300, y=50)

        self.current_experiment_label = tk.Label(self, textvariable=self.current_experiment)
        self.current_experiment_label.place(x=425, y=50)

        self.output_pane = tk.Text(self, wrap='none')
        self.output_pane.place(x=300, y=75)

        self.pack(fill=tk.BOTH, expand=1)

    def cnn_mst(self):
        self.app.test_cnn_mnst()

    def hello(self):
        self.app.test_hello()
        self.call_update()

    def open_file(self):
        path = fd.askopenfilename(
            filetypes=(
                ("Python Tensorflow File", "*.py"),
                ("Tensorflow Checkpoint", "checkpoint"),
                ("All", "*.*"),
            )
        )
        self.file_path.set(path)

    def queue(self):
        self.app.queue_by_path(self.file_path.get())
        self.file_path.set("")

    def load_experiment(self):
        self.app.load_by_path(self.file_path.get())
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

        # Finished experiments
        self.update_listbox(self.app.finished_experiments, self.finished_experiments_listbox)

        # Loaded experiments
        self.update_listbox(self.app.loaded_experiments, self.loaded_experiments_listbox)

        self.call_update()

    def call_update(self):
        self.app.root.after(1000, self.update_elements)

    # Find unaccounted for and populate
    def update_listbox(self, list, listbox):
        front = listbox.size()
        back = len(list)
        if back > front:
            for i in range(front, back):
                listbox.insert(tk.END, list[back - 1].name)


if __name__ == "__main__":
    exit(-1)
