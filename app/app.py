from app.menu import (Menu, MenuController)
from app.player import (Player, PlayerSessionPersistor)
from app.device import Outputs
from app.library import Album
import app.sound

# Menu identifiers are the same as the sound file names (*.ogg)
RING_MENU = [
    "continue",
    "next_chapter",
    "prev_chapter",
    "next_book",
    "prev_book",
    "shutdown"
]

SESSION_PATH = "~/.1buttonplayer.json"

class App:
    def __init__(self, outputs, player, lib):
        self.outputs = outputs
        self.player = player
        self.lib = lib

    def startup(self):
        self._restore_or_clear_session()

        persistor = PlayerSessionPersistor(self.player, SESSION_PATH)
        self.player.add_listener(persistor)

        # Startup complete
        print("Started")
        app.sound.play(app.sound.DeviceSound.boot_complete)

    def _restore_or_clear_session(self):
        if self.player.restore_path(SESSION_PATH):
            return

        print("Starting new session")
        albums = self.lib.all_albums()

        if not albums:
            print("Library is empty :(")
            app.sound.play(app.sound.DeviceSound.library_empty)
            return

        self.player.change_album(albums[0])

    #
    # Menu management
    #

    current_menu = None

    def create_and_show_new_menu(self):
        controller = MenuController(self, self.player)
        self.current_menu = Menu(RING_MENU, controller)
        self.current_menu.present_current_menu_item()

    def is_in_menu(self):
        return self.current_menu != None

    def confirm_selection(self):
        if not self.is_in_menu():
            return
        function_names = globals()
        self.current_menu.call_current_item(function_names)
        self.close_menu()

    #
    # Menu open/close lifecycle
    #

    def open_new_menu(self):
        self.player.pause()
        self.outputs.toggle_blink(True)
        self.create_and_show_new_menu()

    def close_menu(self):
        self.outputs.toggle_blink(False)
        self.current_menu = None

    #
    # Button callbacks
    #

    def button_was_clicked(self):
        if self.is_in_menu():
            self.current_menu.next_menu_item()
            self.current_menu.present_current_menu_item()
        else:
            self.player.play_pause()

    def button_was_held(self):
        if self.is_in_menu():
            self.confirm_selection()
        else:
            self.open_new_menu()

    #
    # Album changes
    #

    def next_album(self):
        album = self.lib.next_album(self.player.current_album())
        self.player.change_album(album)

    def prev_album(self):
        album = self.lib.prev_album(self.player.current_album())
        self.player.change_album(album)
