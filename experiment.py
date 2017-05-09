import os
import queue
import threading

from importlib.machinery import SourceFileLoader


class ConsumerThread(threading.Thread):
    def __init__(self, msg_queue, job_queue):
        threading.Thread.__init__(self)
        self.msg_queue = msg_queue
        self.experiment_queue = job_queue


class Experiment(ConsumerThread):
    def __init__(self, path, msg_queue, job_queue):
        super().__init__(msg_queue, job_queue)
        self.path = path
        self.name = os.path.basename(path)
        self.callable = SourceFileLoader("", path).load_module()
        self.args = []
        self.kwargs = {}
        self.result = ""

    def execute(self):
        self.result = self.callable.__call__(self.args, self.kwargs)

    # overrides the Thread run function
    def run(self):
        try:
            self.execute()
            self.msg_queue.put("Job Completed: " + self.result)
        except queue.Empty:
            pass
