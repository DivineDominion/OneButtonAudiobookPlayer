import time
import pygame.mixer
import os

from sound_helpers import *



class Menu:
    
    delegate = None
    """
    [`identifier`, `regular_sound`, `execute_sound`]
    """
    items = []
    current_index = 0

    def __init__(self, orig_items, delegate):
        def sounds_from_idents(identifier):
            # "continue.ogg" contains the menu title itself when changing selected menu items
            # "ex_continue.ogg" contains the spoken instruction when the selection is confirmed
            fname = identifier + ".ogg"
            ex_fname = "ex_" + identifier + ".ogg"
            return [
                identifier,
                load_sound(menu_sound_path(fname)),
                load_sound(menu_sound_path(ex_fname)),
            ]
        
        self.delegate = delegate
        # Intro sound
        self.items = list(map(sounds_from_idents, orig_items))
        play_sound(load_sound(menu_sound_path("main_menu.ogg")))
        time.sleep(0.5)

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
        print("Selected: " + identifier)
        play_sound(sound)

    def call_current_item(self, function_list):
        identifier, _, exec_sound = self.current_menu_item()
        play_sound(exec_sound)
        # Execute function by name with "on_" prefix to enable `continue`
        mname = "on_" + identifier
        getattr(self.delegate, mname)()
