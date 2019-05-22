import os

class Library:
    def __init__(self, lib_path):
        self.path = os.path.abspath(lib_path)
        self._guard_exists()

    def _guard_exists(self):
        if not (os.path.exists(self.path) \
                and os.path.isdir(self.path)):
            raise Exception("Music library directory does not exist at: %s" % self.path)

    def all_book_dir_paths(self):
        """Returns a sorted list of library subdirectories as absolute paths."""
        self._guard_exists()
        dirs = sorted(os.listdir(self.path))
        absolute_path = lambda d: os.path.join(self.path, d)
        all_paths = map(absolute_path, dirs)
        return [path for path in all_paths if os.path.isdir(path)]
