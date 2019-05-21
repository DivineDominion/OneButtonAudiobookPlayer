#!/usr/bin/env python3

from gpiozero import Button, PWMLED
from signal import pause
from app.sound_helpers import *
from app.app import App
from app.player import Player
from app.device.inputs import Inputs

def main():
    # Initialize playing sounds
    initialize_sound()

    main_led = PWMLED(17)
    player = Player()
    app = App(main_led, player)

    inputs = Inputs()
    inputs.when_button_clicked = app.button_was_clicked
    inputs.when_button_held = app.button_was_held
    
    # Startup complete
    print("Started")
    play_sound(load_sound(device_sound_path("on_boot_complete.ogg")))

    pause()

if __name__ == "__main__":
    main()
