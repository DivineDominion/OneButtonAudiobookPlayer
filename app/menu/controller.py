from subprocess import check_call

class MenuController:

    app = None

    def __init__(self, app, player):
        self.app = app
        self.player = player

    def on_next_chapter(self):
        print("Exec Next Chapter")

    def on_prev_chapter(self):
        print("Exec Prev Chapter")

    def on_next_book(self):
        print("Exec Next Book")

    def on_prev_book(self):
        print("Exec Prev Book")

    def on_shutdown(self):
        print("Exec Shutdown")
        check_call(['sudo', 'poweroff'])

    def on_continue(self):
        print("Exec continue (closing menu)")
        self.close_menu()
        self.player.play()

    def close_menu(self):
        self.app.close_menu()
