#!/usr/bin/env python

from getch import getch, pause
import os

from mpd import (MPDClient, CommandError)
from socket import error as SocketError
from time import sleep

# Configure MPD connection settings
HOST = 'localhost'
PORT = '6600'
CON_ID = {'host':HOST, 'port':PORT}

def mpdConnect(client, con_id):
        client.connect(**con_id)
        return True

def main():
        client = MPDClient()
        client.connect(**CON_ID)
	print(client.status())
	client.play()

        print("Starting loop. Quit with ESC")
	while True: #getch() != ESC:
		print(client.status())
                #if client.status()["state"] == "stop":
                #	client.play()
                #else:
                #        client.pause()
                # sleep(0.1)
                character = ord(getch())
                print(character)
		if character == 27: # ESC or, apparently, arrow keys
                        break

	client.disconnect()

if __name__ == "__main__":
    main()

