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

    def next_album(self, album):
        albums = self.all_albums()
        if not albums:
            print("No albums found in library, returning the current one")
            return album

        try:
            i = albums.index(album)
            if i >= (len(albums) - 1): # Last item, wrap around
                return albums[0]
            return albums[i+1]
        except ValueError:
            print("Reference album not found, starting at the beginning")
            return albums[0]

    def prev_album(self, album):
        albums = self.all_albums()
        if not albums:
            print("No albums found in library, returning the current one")
            return album

        try:
            i = albums.index(album)
            if i <= 0: # First item, wrap around
                return albums[-1]
            return albums[i-1]
        except ValueError:
            print("Reference album not found, starting at the beginning")
            return albums[0]
