import Tkinter as tk
import tkFont as tkfont
from GameObjects.Deck import Deck
from GameObjects.Hand import Hand
from GameObjects.Wallet import Wallet
from GameObjects.Game import Game

game = Game()
player_hand = game.players[0][0]
player_wallet = game.players[0][1]

class BlackJackGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, height=600, width=600)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomePage, BettingPage, PlayerTurn):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Blackjack!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Let's Start the Game!",
                            command=lambda: controller.show_frame("BettingPage"))
        button1.pack()


class BettingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Wallet total
        self.total_label_text = tk.IntVar()
        self.total_label_text.set(player_wallet.amount())
        self.total_label = tk.Label(self, textvariable=self.total_label_text, font=controller.title_font)

        # Wallet label
        self.label = tk.Label(self, text="Wallet:")

        # Buttons
        self.add_button = tk.Button(self, text="Place Bet", command=lambda: self.update("place_bet"))
        #self.subtract_button = tk.Button(self, text="Pay Out", command=lambda: self.update("payout"))
        self.reset_button = tk.Button(self, text="Go Home", command=lambda: controller.show_frame("WelcomePage"))

        # Betting page layout
        self.label.grid(row=0, column=0, sticky=tk.W)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=tk.E)
        self.add_button.grid(row=2, column=0)
        #self.subtract_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2, sticky=tk.W+tk.E)

    # Updates the total
    def update(self, method):
        if method == "place_bet":
            if not game.place_bet(0, 500):
                pass

        self.total_label_text.set(player_wallet.amount())
        self.controller.show_frame("PlayerTurn")


class PlayerTurn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Cards
        self.card_label_text = tk.StringVar()
        self.card_label_text.set(str(game.get_player_hand(0)))
        self.card_label = tk.Label(self, textvariable=self.card_label_text, font=controller.title_font)

        # Card label
        self.cards_label = tk.Label(self, text="Cards:")
        
        # Card total
        self.card_total_label = tk.Label(self, text="Your hand is valued at:")
        self.card_total_text = tk.IntVar()
        self.card_total_text.set(game.players[0][0].get_total())
        self.total_label = tk.Label(self, textvariable=self.card_total_text, font=controller.title_font)

        # Buttons
        self.hit_button = tk.Button(self, text="Hit!", command=lambda: self.update("hit"))
        self.stay_button = tk.Button(self, text="Stay!", command=lambda: self.update("stay"))
        self.reset_button = tk.Button(self, text="Go Home", command=lambda: controller.show_frame("WelcomePage"))

        # PlayerTurn layout
        self.cards_label.grid(row=0, column=0, sticky=tk.W)
        self.card_label.grid(row=0, column=1, columnspan=2, sticky=tk.E)
        self.card_total_label.grid(row=1, column=0, sticky=tk.W)
        self.total_label.grid(row=1, column=1, columnspan=2, sticky=tk.E)
        self.hit_button.grid(row=3, column=0)
        self.stay_button.grid(row=3, column=1)
        self.reset_button.grid(row=3, column=2, sticky=tk.W+tk.E)

    # Updates the total
    def update(self, method):
        if method == "hit":
            game.player_hit(0)
        elif method == "stay":
            self.cards -= 1

        self.card_label_text.set(str(game.get_player_hand(0)))
        self.card_total_text.set(game.players[0][0].get_total())


if __name__ == "__main__":
    app = BlackJackGUI()
    app.mainloop()

