from app.device.outputs import Outputs
from app.player.mpdadapter import MPDAdapter
from app.player.session import Session

class Player:
    def __init__(self, outputs, mpd_adapter = MPDAdapter()):
        self.outputs = outputs
        self.mpd_adapter = mpd_adapter
        self._listeners = []

    def add_listener(self, listener):
        self._listeners.append(listener)

    def fire(self, message):
        mname = "on_" + message
        handler = lambda obj: getattr(obj, mname)
        calls = [handler(l) for l in self._listeners
                 if handler(l) is not None]
        for callback in calls:
            callback(self)

    def is_playing(self):
        return self.mpd_adapter.is_playing()

    def pause(self):
        if self.is_playing():
            self.outputs.toggle_light(False)
            self.mpd_adapter.pause()
            self.fire("pause")

    def play(self):
        if not self.is_playing():
            self.outputs.toggle_light(True)
            self.mpd_adapter.play()
            self.fire("play")

    def play_pause(self):
        if self.is_playing():
            self.pause()
        else:
            self.play()
        print("Is playing now: " + str(self.is_playing()))

    def next_song(self, autoplay = True):
        self.mpd_adapter.next()
        if autoplay and not self.is_playing():
            self.play()

    def prev_song(self, autoplay = True):
        self.mpd_adapter.previous()
        if autoplay and not self.is_playing():
            self.play

    def current_session(self):
        return Session(elapsed=self.mpd_adapter.elapsed(),
                       songid=self.mpd_adapter.songid())

    def restore(self, session):
        if not session:
            return False

        return self.mpd_adapter.seekid(songid=session.songid,
                                       time=session.elapsed)

    def restore_path(self, path):
        return self.restore(Session.from_file(path))
