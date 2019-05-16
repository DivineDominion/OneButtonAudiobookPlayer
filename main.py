#!/usr/bin/env python3

from gpiozero import Button, PWMLED
from signal import pause
from app.sound_helpers import *
from app.app import App
from app.player import Player

def main():
    # Initialize playing sounds
    initialize_sound()
    
    main_led = PWMLED(17)
    player = Player()
    app = App(main_led, player)

    main_btn = Button(2, hold_time=2)
    main_btn.when_held = app.button_was_held
    main_btn.when_released = app.button_was_released
    
    # Startup complete
    print("Started")
    play_sound(load_sound(device_sound_path("on_boot_complete.ogg")))

    pause()

if __name__ == "__main__":
    main()
