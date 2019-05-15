from menu.controller import MenuController
from menu.menu import Menu

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

    led = None
    def __init__(self, led):
        self.led = led

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

    is_playing = False
    def pause(self):
        if self.is_playing:
            self.toggle_light(False)
            self.is_playing = False

    def play(self):
        if not self.is_playing:
            self.toggle_light(True)
            self.is_playing = True

    def play_pause(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()
        print("Is playing now: " + str(self.is_playing))
    
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
        self.pause()
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
    
    did_hold = False
    def button_was_released(self):
        if not self.did_hold:
            self.button_was_clicked()
        self.did_hold = False

    def button_was_clicked(self):
        if self.is_in_menu():
            self.current_menu.next_menu_item()
            self.current_menu.present_current_menu_item()
        else:
            self.play_pause()

    def button_was_held(self):
        self.did_hold = True
        if self.is_in_menu():
            self.confirm_selection()
        else:
            self.open_new_menu()
