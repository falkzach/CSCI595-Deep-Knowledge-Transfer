#!/usr/bin/env python

import os
from importlib.machinery import SourceFileLoader
import queue
import threading
import tkinter as tk
from tkinter import messagebox

import frontend

#TODO: our experiment, fine way to import by file
import mnist_deep
import test1
import hello

class ConsumerThread(threading.Thread):

    def __init__(self, msg_queue, job_queue):
        threading.Thread.__init__(self)
        self.msg_queue = msg_queue
        self.job_queue = job_queue

    # overrides the Thread run function
    def run(self):
        try:
            callable, args, kwargs = self.job_queue.get_nowait()
            result = callable.__call__(args, kwargs)
            self.msg_queue.put("Callable Completed: " + result)
        except queue.Empty:
            pass


# Base Application class
class APP(object):

    def __init__(self):
        # queues exist in main thread
        self.msg_queue = queue.Queue()
        self.job_queue = queue.Queue()
        self.job = None
        self.finished_jobs = []

    # called after the TK event loop by call
    def process_queues(self):
        try:
            # check if there is a job in queue and no job running
            if (not self.job_queue.empty()):
                if (self.job is None):
                    print("?test?")
                    self.job = ConsumerThread(self.msg_queue, self.job_queue)
                    self.job.start()

            if (not self.job.isAlive()):
                self.job.join()
                self.finished_jobs.append(self.job)
                self.job = None
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

    def submit_job(self, callable, args=[], kwargs ={}):
        self.job_queue.put((callable, args, kwargs))

    def test_job(self):
        self.submit_job(test1)

    def test_cnn_mnst(self):
        self.submit_job(mnist_deep)

    def test_hello(self):
        self.submit_job(hello)

    def queue_by_path(self, path):
        if ( os.path.isfile(path) ):
            foo = SourceFileLoader("", path).load_module()
            self.submit_job(foo)



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
        self.root.geometry("800x500+300+300")  # TODO: extract app layout dimensions

        # initiate our frontend
        self.frontend = frontend.Frontend(self.root, self)

        # begin processor
        self.call_thread()

        # handle closeing window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # run tk main loop
        self.root.mainloop()

    # tk implementation of call_thread, calls after the main tk event loop
    def call_thread(self):
        self.root.after(100, self.process_queues)

    def on_close(self):
        if(self.job is None):
            self.root.destroy()

        elif(self.job.isAlive() or ( self.job is ConsumerThread and not self.job_queue.empty() ) ):
            if messagebox.askokcancel("Quit", "Jobs still running, are you sure you want to quit?"):
                self.root.destroy()
