import os
from .album import Album

class Library:
    def __init__(self, lib_path):
        self.path = os.path.abspath(lib_path)
        self._guard_exists()

    def _guard_exists(self):
        if not (os.path.exists(self.path) \
                and os.path.isdir(self.path)):
            raise Exception("Music library directory does not exist at: %s" % self.path)

    def all_albums(self):
        """Returns a list of Album objects in the library subdirectories, sorted by name."""
        self._guard_exists()
        return [Album(rel_path=path)
                for path in sorted(os.listdir(self.path))
                if os.path.isdir(os.path.join(self.path, path))]
