class Player:

    def __init__(self):
        self._is_playing = False

    def is_playing(self):
        return self._is_playing
    
    def pause(self):
        if self.is_playing():
            self.toggle_light(False)
            self._is_playing = False

    def play(self):
        if not self.is_playing():
            self.toggle_light(True)
            self._is_playing = True

    def play_pause(self):
        if self.is_playing():
            self.pause()
        else:
            self.play()
        print("Is playing now: " + str(self.is_playing()))
