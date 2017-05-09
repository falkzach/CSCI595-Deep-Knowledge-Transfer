import os
import queue
import threading

from importlib.machinery import SourceFileLoader


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
            self.msg_queue.put("Job Completed: " + result)
        except queue.Empty:
            pass


class Job:
    def __init__(self, path):
        self.path = path
        self.name = os.path.splitext(path)[0]
        self.callable = SourceFileLoader("", path).load_module()
        self.args = []
        self.kwargs = {}

    def run(self):
        return self.callable.__call__(self.args, self.kwargs)
