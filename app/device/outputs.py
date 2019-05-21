from gpiozero import PWMLED
from app.device.statusled import StatusLED

class Outputs:

    def __init__(self):
        self.status_led = StatusLED(PWMLED(17))

    #
    # LED Adapter
    #
    
    def toggle_light(self, is_on):
        self.status_led.toggle_light(is_on)

    def toggle_blink(self, is_blinking):
        self.status_led.toggle_blink(is_blinking)
