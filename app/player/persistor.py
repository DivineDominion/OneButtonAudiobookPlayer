from app.player.player import Player
from app.player.session import Session

class PlayerSessionPersistor:
    def __init__(self, player, path):
        self.path = path
        self.player = player

    def on_play(self, player):
        self.store_session(player)

    def on_pause(self, player):
        self.store_session(player)

    def store_session(self, player):
        player.current_session().write(self.path)
