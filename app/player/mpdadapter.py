import mpd

HOST = "localhost"
PORT = 6600

class MPDAdapter:
    def __init__(self):
        self.client = mpd.MPDClient()
        self.client.connect(HOST, PORT)
        print("MPD: " + self.client.mpd_version)
        print(self.client.status())

    def __del__(self):
        print("Closing MPD connection ...")
        self.client.close()
        self.client.disconnect()

    def is_playing(self):
        return self.client.status()["state"] == "play"

    def play(self):
        self.client.play()

    def pause(self):
        self.client.pause()

    def next(self):
        self.client.next()

    def previous(self):
        self.client.previous()

    def songid(self):
        return self.client.status()["songid"]

    def elapsed(self):
        return self.client.status()["elapsed"]

    def seekid(self, songid, time):
        try:
            self.client.seekid(songid, time)
            return True
        except mpd.base.CommandError as e:
            # Could not read song ID or playlist
            print("Failed to seek to songid '%s' at '%s's: %s" % (songid, time, e))
            return False

    def replace_playlist(self, rel_path):
        self.client.clear()
        self.client.add(rel_path)
        self._remove_album_voiceover()
        
    def _remove_album_voiceover(self):
        """Removes the voice-over for a playlist, `_title.*` per convention."""
        meta_file = self.client.playlistsearch("filename", "_title")
        if meta_file:
            self.client.deleteid(meta_file[0]["id"])
