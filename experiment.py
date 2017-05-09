import os
import queue
import threading

from importlib.machinery import SourceFileLoader

from session_checkpointer import Checkpointer


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
        self.session = None
        self.session_checkpointer = None

    def execute(self):
        try:
            self.result, self.session = self.callable.__call__(self.args, self.kwargs)
        except TypeError:
            print("No result returned from the experimented " + self.name + "!")

    # overrides the Thread run function
    def run(self):
        try:
            self.execute()
            self.msg_queue.put("Job Completed: " + self.result)
            self.session_checkpointer = Checkpointer(self.session)
            self.session_checkpointer.save_model(self)
        except queue.Empty:
            pass

    def get_save_name(self):
        return self.name.split('.')[0] + ".session"

    def get_save_path(self):
        return self.name.split('.')[0] + "/"


if __name__ == "__main__":
    exit(-1)
