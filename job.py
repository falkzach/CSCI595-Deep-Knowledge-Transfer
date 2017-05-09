import ntpath


class Job:
    def __init__(self, path):
        self.path = path
        self.name = self._path_leaf(path)
        self.runnable = None

    def _path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)