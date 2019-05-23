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
        self.client.seekid(songid, time)
