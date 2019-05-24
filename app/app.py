from app.menu.controller import MenuController
from app.menu.menu import Menu
from app.player.player import Player
from app.device.outputs import Outputs
from app.player.persistor import PlayerSessionPersistor
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
    def __init__(self, outputs, player):
        self.outputs = outputs
        self.player = player

    def startup(self):
        self.player.restore_path(SESSION_PATH)

        persistor = PlayerSessionPersistor(self.player, SESSION_PATH)
        self.player.add_listener(persistor)

        # Startup complete
        print("Started")
        app.sound.play(app.sound.DeviceSound.boot_complete)

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
