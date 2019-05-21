from gpiozero import Button

class ClickHoldButtonRelay:
    
    def __init__(self, button):
        self.button = button
        self.button.when_held = self.button_was_held
        self.button.when_released = self.button_was_released
        self.did_hold = False    
        
    def button_was_released(self):
        if not self.did_hold:
            self.button_was_clicked()
        self.did_hold = False

    def button_was_clicked(self):
        if self.when_clicked:
            self.when_clicked()

    def button_was_held(self):
        self.did_hold = True
        if self.when_held:
            self.when_held()

    @property
    def when_clicked(self):
        return self._when_clicked

    @when_clicked.setter
    def when_clicked(self, value):
        # consider wrapping/unwrapping callbacks like GPIOZERO: https://github.com/RPi-Distro/python-gpiozero/blob/7b67374fd0c8c4fde5586d9bad9531f076db9c0c/gpiozero/mixins.py#L299
        self._when_clicked = value

    @property
    def when_held(self):
        return self._when_held

    @when_held.setter
    def when_held(self, value):
        self._when_held = value

