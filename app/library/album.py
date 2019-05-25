import os

class Album:
    def __init__(self, path):
        self.path = path

    def name(self):
        return os.path.basename(self.path)
