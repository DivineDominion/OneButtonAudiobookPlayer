import mpd

HOST = "localhost"
PORT = 6600

class MPDAdapter:
    def __init__(self):
        self.client = mpd.MPDClient()
        self._connect()

    def _connect(self):
        self.client.connect(HOST, PORT)
        print("MPD: " + self.client.mpd_version)
        print("Updating ...")
        self.client.update()
        print("Status: %s" % self.client.status())

    def __del__(self):
        print("Closing MPD connection ...")
        try:
            self.client.close()
            self.client.disconnect()
        except mpd.base.ConnectionError:
            pass

    def _reconnecting(func):
        def wrapper_reconnect(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except mpd.base.ConnectionError:
                print("Connection lost, reconnecting and retrying ...")
                self = args[0]
                self._connect()
                return func(*args, **kwargs)
        return wrapper_reconnect

    @_reconnecting
    def is_playing(self):
        return self.client.status()["state"] == "play"

    @_reconnecting
    def play(self):
        self.client.play()

    @_reconnecting
    def pause(self):
        self.client.pause()

    @_reconnecting
    def next(self):
        self.client.next()

    @_reconnecting
    def previous(self):
        self.client.previous()

    @_reconnecting
    def songid(self):
        return self.client.status()["songid"]

    @_reconnecting
    def elapsed(self):
        return self.client.status()["elapsed"]

    @_reconnecting
    def seekid(self, songid, time):
        try:
            self.client.seekid(songid, time)
            return True
        except mpd.base.CommandError as e:
            # Could not read song ID or playlist
            print("Failed to seek to songid '%s' at '%s's: %s" % (songid, time, e))
            return False

    @_reconnecting
    def replace_playlist(self, rel_path):
        self.client.clear()
        self.client.add(rel_path)
        self._remove_album_voiceover()

    def _remove_album_voiceover(self):
        """Removes the voice-over for a playlist, `_title.*` per convention."""
        meta_file = self.client.playlistsearch("filename", "_title")
        if meta_file:
            self.client.deleteid(meta_file[0]["id"])
