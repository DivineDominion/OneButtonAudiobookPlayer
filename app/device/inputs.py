from app.device.buttonrelay import ClickHoldButtonRelay
from gpiozero import Button

class Inputs:

    def __init__(self):
        self.relay = ClickHoldButtonRelay(Button(2, hold_time=2))
        self.relay.when_clicked = self._fire_button_was_clicked
        self.relay.when_held = self._fire_button_was_held
        
        self._when_button_clicked = None
        self._when_button_held = None

    def _fire_button_was_clicked(self):
        if self.when_button_clicked:
            self.when_button_clicked()
            
    @property
    def when_button_clicked(self):
        return self._when_button_clicked

    @when_button_clicked.setter
    def when_button_clicked(self, value):
        # consider wrapping/unwrapping callbacks like GPIOZERO: https://github.com/RPi-Distro/python-gpiozero/blob/7b67374fd0c8c4fde5586d9bad9531f076db9c0c/gpiozero/mixins.py#L299
        self._when_button_clicked = value

    def _fire_button_was_held(self):
        if self.when_button_held:
            self.when_button_held()

    @property
    def when_button_held(self):
        return self._when_button_held

    @when_button_held.setter
    def when_button_held(self, value):
        self._when_button_held = value

