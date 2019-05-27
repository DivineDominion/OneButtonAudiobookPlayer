from .mpdadapter import MPDAdapter
from .session import Session
from app.device import Outputs
from app.library import Album

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
        return Session(album=self.album,
                       songid=self.mpd_adapter.songid(),
                       elapsed=self.mpd_adapter.elapsed())

    def restore(self, session):
        if not session:
            return False

        self.album = session.album
        return self.mpd_adapter.seekid(songid=session.songid,
                                       time=session.elapsed)

    def restore_path(self, path):
        return self.restore(Session.from_file(path))

    def change_album(self, album):
        print("Changing to album \"%s\"" % album.name())
        self.album = album
        self.mpd_adapter.replace_playlist(rel_path=album.rel_path)
