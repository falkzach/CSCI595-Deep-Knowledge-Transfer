import os
import queue
import threading

from importlib.machinery import SourceFileLoader


class ConsumerThread(threading.Thread):
    def __init__(self, msg_queue, job_queue):
        threading.Thread.__init__(self)
        self.msg_queue = msg_queue
        self.experiment_queue = job_queue

    # overrides the Thread run function
    def run(self):
        try:
            job = self.experiment_queue.get_nowait()
            job.run()
            self.msg_queue.put("Job Completed: " + job.result)
        except queue.Empty:
            pass


class Experiment:
    def __init__(self, path):
        self.path = path
        self.name = os.path.splitext(path)[0]
        self.callable = SourceFileLoader("", path).load_module()
        self.args = []
        self.kwargs = {}
        self.result = ""

    def run(self):
        self.result = self.callable.__call__(self.args, self.kwargs)
