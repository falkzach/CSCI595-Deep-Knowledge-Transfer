import os
import queue
import threading
import tensorflow as tf

from importlib.machinery import SourceFileLoader

import time

from checkpoint import SaveCheckpoint, LoadCheckpoint


class Experiment(threading.Thread):
    def __init__(self, msg_queue, job_queue):
        threading.Thread.__init__(self)
        self.msg_queue = msg_queue
        self.experiment_queue = job_queue

        self.session = None
        self.session_checkpoint = None


def get_opoch_time():
    return str(int(time.time()))


class PythonExperiment(Experiment):
    def __init__(self, path, msg_queue, job_queue):
        super().__init__(msg_queue, job_queue)
        self.path = path
        self.name = os.path.basename(path)
        self.callable = SourceFileLoader("", path).load_module()
        self.args = []
        self.kwargs = {}
        self.result = ""

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
            self.session_checkpoint = SaveCheckpoint()
            self.session_checkpoint.save_model(self)
        except queue.Empty:
            pass

    def get_save_name(self):
        return self.name.split('.')[0] + "-" + get_opoch_time() +".session"

    def get_save_path(self):
        return self.name.split('.')[0] + "-" + get_opoch_time() + "/"


class CheckpointExperiment(Experiment):
    def __init__(self, path, msg_queue, experiment_queue):
        super().__init__(msg_queue, experiment_queue)
        self.path = path
        self.pwd = os.path.dirname(os.path.realpath(path))
        self.name = os.path.basename(self.pwd)

        self.session_checkpoint = LoadCheckpoint(self.pwd, self.name)

    def run(self):
        pass


if __name__ == "__main__":
    exit(-1)
