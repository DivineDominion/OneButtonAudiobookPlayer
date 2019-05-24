import os
import json

class Session:

    @staticmethod
    def from_file(path):
        abspath = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(abspath):
            return None

        with open(abspath, 'r') as fp:
            data = json.load(fp)
            return Session(elapsed=data["elapsed"],
                           songid=data["songid"])

    def __init__(self, elapsed, songid):
        self.elapsed = elapsed
        self.songid = songid

    def data(self):
        return {
            "elapsed": self.elapsed,
            "songid": self.songid
        }

    def write(self, path):
        with open(os.path.abspath(os.path.expanduser(path)), 'w') as fp:
            json.dump(self.data(), fp)
