from gpiozero import PWMLED

class StatusLED:
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
