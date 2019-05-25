import os

class Album:
    def __init__(self, rel_path):
        self.rel_path = rel_path

    def name(self):
        return os.path.basename(self.rel_path)
