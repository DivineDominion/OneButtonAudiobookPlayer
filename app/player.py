import mpd
from app.device.outputs import Outputs

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


class Player:
    def __init__(self, outputs, mpd_adapter = MPDAdapter()):
        self.outputs = outputs
        self.mpd_adapter = mpd_adapter

    def is_playing(self):
        return self.mpd_adapter.is_playing()

    def pause(self):
        if self.is_playing():
            self.outputs.toggle_light(False)
            self.mpd_adapter.pause()

    def play(self):
        if not self.is_playing():
            self.outputs.toggle_light(True)
            self.mpd_adapter.play()

    def play_pause(self):
        if self.is_playing():
            self.pause()
        else:
            self.play()
        print("Is playing now: " + str(self.is_playing()))
