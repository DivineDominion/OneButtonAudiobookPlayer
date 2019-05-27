from subprocess import check_call

class MenuController:

    app = None

    def __init__(self, app, player):
        self.app = app
        self.player = player

    def close_menu(self):
        self.app.close_menu()

    #
    # Callbacks
    #

    def on_next_chapter(self):
        print("Exec Next Chapter")
        self.player.next_song()

    def on_prev_chapter(self):
        print("Exec Prev Chapter")
        self.player.prev_song()

    def on_next_book(self):
        print("Exec Next Book")
        self.app.next_album()
        self.player.play()

    def on_prev_book(self):
        print("Exec Prev Book")

    def on_shutdown(self):
        print("Exec Shutdown")
        check_call(['sudo', 'poweroff'])

    def on_continue(self):
        print("Exec continue (closing menu)")
        self.close_menu()
        self.player.play()
