#!/usr/bin/env python

import os
import queue
import sys

import tkinter as tk
from tkinter import messagebox

import frontend
import job
import ioredirect


# Base Application class
class APP(object):
    def __init__(self):
        # queues exist in main thread
        self.msg_queue = queue.Queue()
        self.job_queue = queue.Queue()
        self.tf_thread = None
        self.finished_jobs = []

    # called after the TK event loop by call
    def process_queues(self):
        try:
            # check if there is a job in queue and no job running
            if not self.job_queue.empty():
                if self.tf_thread is None:
                    self.tf_thread = job.ConsumerThread(self.msg_queue, self.job_queue)
                    self.tf_thread.start()

            if not self.tf_thread.isAlive():
                self.tf_thread.join()
                self.finished_jobs.append(self.tf_thread)
                self.tf_thread = None
        except:
            pass

        try:
            msg = self.msg_queue.get_nowait()
            print(msg)
        except:
            pass

        self.call_thread()

    # abstract, to be implemented in concrete Applications
    def call_thread(self):
        pass

    def submit_job(self, job):
        self.job_queue.put(job)

    def queue_by_path(self, path):
        if os.path.isfile(path):
            experiment = job.Job(path)
            if "__call__" in dir(experiment.callable):
                self.submit_job(experiment)
            else:
                print("__call__ not defined for " + path)

    def test_cnn_mnst(self):
        self.queue_by_path(os.path.abspath("tests/mnist_deep.py"))

    def test_hello(self):
        self.queue_by_path(os.path.abspath("tests/hello.py"))

# CLI implementation of the application
class CLI(APP):
    pass


# GUI implementation of the application
class GUI(APP):
    def __init__(self):
        super().__init__()

        # initiate tk interactive
        self.root = tk.Tk()
        self.root.title("TF Knowledge Transfer")  # TODO: extract app name
        self.root.geometry("1200x700+300+300")  # TODO: extract app layout dimensions
        self.root.configure(background='black')

        # initiate our frontend
        self.frontend = frontend.Frontend(self.root, self)

        # redirect STDOUT
        sys.stdout = ioredirect.TkIoRedirect(self.frontend.get_output_pane())

        # begin processor
        self.call_thread()

        # handle closeing window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # update watcher
        self.frontend.call_update()

        # run tk main loop
        self.root.mainloop()

    # tk implementation of call_thread, calls after the main tk event loop
    def call_thread(self):
        self.root.after(100, self.process_queues)

    def on_close(self):
        if self.tf_thread is None:
            self.exit()

        elif self.tf_thread.isAlive() or (self.tf_thread is job.ConsumerThread and not self.job_queue.empty()):
            if messagebox.askokcancel("Quit", "Jobs still running, are you sure you want to quit?"):
                self.exit()

    def exit(self):
        # TODO: interupt running job
        self.root.destroy()
        sys.exit()
