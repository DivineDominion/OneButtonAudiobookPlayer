import pygame.mixer
import time
import os

def initialize_sound():
    if not pygame.mixer.get_init():
        pygame.mixer.init()

initialize_sound()


def load(path):
    return pygame.mixer.Sound(path)

def play(sound):
    channel = sound.play()
    while channel.get_busy() == True:
        pygame.time.wait(100)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCE_PATH = os.path.join(MODULE_PATH, "..", "assets")
MENU_SOUNDS_PATH = os.path.join(RESOURCE_PATH, "menu_sounds")
DEVICE_SOUNDS_PATH = os.path.join(RESOURCE_PATH, "device_sounds")

def menu_sound_path(filename):
    return os.path.join(MENU_SOUNDS_PATH, filename)

def device_sound_path(filename):
    return os.path.join(DEVICE_SOUNDS_PATH, filename)

class DeviceSound:
    boot_complete = load(device_sound_path("on_boot_complete.ogg"))
    library_empty = load(device_sound_path("on_library_empty.ogg"))
