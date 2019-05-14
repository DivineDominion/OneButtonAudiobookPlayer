from gpiozero import Button, PWMLED
from subprocess import check_call
from signal import pause
import pygame.mixer

def play_sound(sound):
    channel = sound.play()
    while channel.get_busy() == True:
        pygame.time.wait(100)

class Menu:
    delegate = None
    """
    [`identifier`, `regular_sound`, `execute_sound`]
    """
    items = []
    current_index = 0

    def __init__(self, items, delegate):
        def sounds_from_idents(identifier):
            fname = identifier + ".ogg"
            ex_fname = "ex_" + identifier + ".ogg"
            return [
                identifier,
                pygame.mixer.Sound("menu_sounds/" + fname),
                pygame.mixer.Sound("menu_sounds/" + ex_fname),
            ]
        self.delegate = delegate
        self.items = map(sounds_from_idents, items)
        # Intro sound
        play_sound(pygame.mixer.Sound("menu_sounds/main_menu.ogg"))

    def item_count(self):
        return len(self.items)

    def next_menu_item(self):
        self.current_index += 1
        if self.current_index >= self.item_count():
            self.current_index = 0

    def prev_menu_item(self):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = self.item_count() - 1

    def current_menu_item(self):
        """
        Returns `[identifier, sound_title, sound_execute]`
        """
        return self.items[self.current_index]

    def present_current_menu_item(self):
        identifier, sound, _ = self.current_menu_item()
        print "Selected: " + identifier
        play_sound(sound)

    def call_current_item(self, function_list):
        identifier, _, exec_sound = self.current_menu_item()
        play_sound(exec_sound)
        # Execute function by name with "on_" prefix to enable `continue`
        mname = "on_"+identifier
        getattr(self.delegate, mname)()

##############################################################################
# Input / Output control
##############################################################################

# sound_file_name
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

    current_menu = None
    def is_in_menu(self):
        return self.current_menu != None

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
        print "Is playing now: " + str(self.is_playing)

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

    def confirm_selection(self):
        if not self.is_in_menu():
            return
        function_names = globals()
        self.current_menu.call_current_item(function_names)
        self.close_menu()

    def open_new_menu(self):
        self.pause()
        self.toggle_blink(True)
        self.current_menu = Menu(RING_MENU, self)
        self.current_menu.present_current_menu_item()

    def close_menu(self):
        self.toggle_blink(False)
        self.current_menu = None

    # Menu action (delegate calls)
    
    def on_next_chapter(self):
        print "Exec Next Chapter"

    def on_prev_chapter(self):
        print "Exec Prev Chapter"

    def on_next_book(self):
        print "Exec Next Book"

    def on_prev_book(self):
        print "Exec Prev Book"

    def on_shutdown(self):
        print "Exec Shutdown"
        check_call ['sudo', 'poweroff']

    def on_continue(self):
        print "Exec continue (closing menu)"
        self.close_menu()

##############################################################################

def main():
    pygame.mixer.init()
    main_led = PWMLED(17)
    main_btn = Button(2, hold_time=3)
    app = App(main_led)
    main_btn.when_held = app.button_was_held
    main_btn.when_released = app.button_was_released
    print "Started"
    pause()

if __name__ == "__main__":
    main()
