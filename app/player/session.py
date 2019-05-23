import os
import json

class Session:

    def __init__(self, elapsed, songid):
        self.elapsed = elapsed
        self.songid = songid

    def data(self):
        return {
            "elapsed": self.elapsed,
            "songid": self.songid
        }

    def read(self, path):
        with open(os.path.abspath(os.path.expanduser(path)), 'r') as fp:
            data = json.load(fp)
            self.elapsed = data["elapsed"]
            self.songid = data["songid"]

    def write(self, path):
        with open(os.path.abspath(os.path.expanduser(path)), 'w') as fp:
            json.dump(self.data(), fp)
