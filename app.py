#!/usr/bin/env python

import queue
import threading
import tkinter as tk

import compute
import frontend


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
class APP:

    def __init__(self):
        # queues exist in main thread
        self.msg_queue = queue.Queue()
        self.job_queue = queue.Queue()

    def process_queues(self):
        try:
            if (not self.job_queue.empty()):
                ConsumerThread(self.msg_queue, self.job_queue).start()
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
        self.submit_job(compute)


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

        # run tk main looop
        self.root.mainloop()

    def call_thread(self):
        self.root.after(100, self.process_queues) # 100ms delay instead of unnecessary continuous processing
