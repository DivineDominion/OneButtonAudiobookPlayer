import pygame.mixer
import time

def load_sound(path):
    return pygame.mixer.Sound(path)

def play_sound(sound):
    channel = sound.play()
    while channel.get_busy() == True:
        pygame.time.wait(100)
