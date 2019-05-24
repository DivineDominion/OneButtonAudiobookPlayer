#!/usr/bin/env python3

from signal import pause
from app.app import App
from app.player.player import Player
from app.device.inputs import Inputs
from app.device.outputs import Outputs
from app.library import Library

def main():
    outputs = Outputs()
    app = App(outputs=outputs,
              player=Player(outputs))

    inputs = Inputs()
    inputs.when_button_clicked = app.button_was_clicked
    inputs.when_button_held = app.button_was_held

    app.startup()
    pause()

if __name__ == "__main__":
    main()
