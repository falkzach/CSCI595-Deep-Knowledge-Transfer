#!/usr/bin/env python

import tkinter as tk
import queue
import threading
import frontend

import compute
import time


class ThreadTask(threading.Thread):

    def __init__(self, msg_queue, job_queue):
        threading.Thread.__init__(self)

        # give task thread access to queues from main thread
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


class GUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("TF Knowledge Transfer")  # TODO: extract app name
        self.root.geometry("800x500+300+300")  # TODO: extract app layout dimensions

        self.frontend = frontend.Frontend(self.root, self)

        # queues exist in main thread
        self.msg_queue = queue.Queue()
        self.job_queue = queue.Queue()

        self.call_thread()
        self.root.mainloop()

    def process_queues(self):
        try:
            if(not self.job_queue.empty()):
                ThreadTask(self.msg_queue, self.job_queue).start()
        except:
            pass

        try:
            msg = self.msg_queue.get_nowait()
            print(msg)
        except:
            pass

        self.call_thread()


    def call_thread(self):
        self.root.after(100, self.process_queues) # 100ms delay instead of unnecessary continuous processing

    def submit_job(self, callable, args = [], kwargs = {}):
        self.job_queue.put((callable, args, kwargs))

    def test_job(self):
        self.submit_job(compute)
