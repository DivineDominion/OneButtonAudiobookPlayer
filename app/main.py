#!/usr/bin/env python3

from gpiozero import Button, PWMLED
from signal import pause
from sound_helpers import *
from app import App

def main():
    # Initialize playing sounds
    initialize_sound()
    
    main_led = PWMLED(17)
    app = App(main_led)

    main_btn = Button(2, hold_time=2)
    main_btn.when_held = app.button_was_held
    main_btn.when_released = app.button_was_released
    
    # Startup complete
    print("Started")
    play_sound(load_sound(device_sound_path("on_boot_complete.ogg")))

    pause()

if __name__ == "__main__":
    main()
