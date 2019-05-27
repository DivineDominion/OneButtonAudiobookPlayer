import os
import json
from app.library import Album

class Session:
    @staticmethod
    def from_file(path):
        abspath = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(abspath):
            return None

        with open(abspath, 'r') as fp:
            try:
                data = json.load(fp)
                return Session(album=Album(rel_path=data["album"]),
                               songid=data["songid"],
                               elapsed=data["elapsed"])
            except (json.decoder.JSONDecodeError, KeyError) as e:
                print("Error loading from \"%s\": %s" % (abspath, e))
                return None

    def __init__(self, album, songid, elapsed):
        self.album = album
        self.songid = songid
        self.elapsed = elapsed

    def data(self):
        return {
            "album": self.album.rel_path,
            "elapsed" : self.elapsed,
            "songid" : self.songid
        }

    def write(self, path):
        with open(os.path.abspath(os.path.expanduser(path)), 'w') as fp:
            json.dump(self.data(), fp)
