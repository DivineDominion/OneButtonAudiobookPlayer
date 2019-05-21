from app.menu.controller import MenuController
from app.menu.menu import Menu
from app.player import Player

# Menu identifiers are the same as the sound file names (*.ogg)
RING_MENU = [
    "continue",
    "next_chapter",
    "prev_chapter",
    "next_book",
    "prev_book",
    "shutdown"
]

class App:

    def __init__(self, led, player):
        self.led = led
        self.player = player

    def toggle_light(self, is_on):
        if is_on:
            self.led.value = 0.5
        else:
            self.led.off()

    def toggle_blink(self, is_blinking):
        if is_blinking:
            self.led.blink()
        else:
            self.led.off()

    #
    # Menu management
    #
   
    current_menu = None
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
        self.toggle_blink(True)
        controller = MenuController(self)
        self.current_menu = Menu(RING_MENU, controller)
        self.current_menu.present_current_menu_item()

    def close_menu(self):
        self.toggle_blink(False)
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
