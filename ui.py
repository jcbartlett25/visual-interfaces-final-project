################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################
import Tkinter as tk
import tkFont as tkfont
from GameObjects.Deck import Deck
from GameObjects.Hand import Hand
from GameObjects.Wallet import Wallet
from GameObjects.Game import Game
from recognition import GestureRecognizer
import time

game = Game()
player_hand = game.players[0][0]
player_wallet = game.players[0][1]
SHUFFLE_LIMIT = 60
gesture_recognizer = GestureRecognizer()

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
        for F in (WelcomePage, BettingPage, PlayerTurn, DealerTurn, PayoutScreen):
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
        frame = self.frames[page_name].show()
        frame.tkraise()
        #time.sleep(1)
        
        if page_name == 'DealerTurn':
            frame.dealer_turn()
            #print('hi')
        elif page_name == 'PayoutScreen':
            frame.payout()
            #print(gesture_recognizer.look_for_gesture())
        elif page_name == 'PlayerTurn':
            frame.play_turn()
        else:
            frame.advance()


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Blackjack!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Let's Start the Game!",
                            command=lambda: controller.show_frame("BettingPage"))
        button1.pack()

    def show(self):
        return self

    def advance(self):
        gesture_recognizer.wait_for_fist()
        self.controller.show_frame("BettingPage")



class BettingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Wallet total
        self.total_label_text = tk.StringVar()
        self.total_label_text.set(0)
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
        self.reset_button.grid(row=2, column=2, sticky=tk.W+tk.E)

    # Updates the total
    def update(self, method):
        if method == "place_bet":
            if not game.place_bet(0, 500):
                pass

        self.total_label_text.set(player_wallet.amount())
        self.controller.show_frame("PlayerTurn")

    def show(self):
        
        # New round, clear everyone's hands
        game.clear_hands()

        # Reshuffle the deck when the limit is reached
        if len(game.deck) < SHUFFLE_LIMIT:
            print('Reshuffling cards...Done')
            game.reshuffle_deck()

        # Deal everyone in the game 2 cards
        game.deal_cards()
        game.deal_cards()

        if player_wallet.amount() < 500:
            self.total_label_text.set('You do not have enough coins...')
            self.add_button.grid_forget()
            return self

        self.total_label_text.set(str(player_wallet.amount()))

        return self

    def advance(self):
        gesture_recognizer.wait_for_fist()
        game.place_bet(0, 500)
        self.controller.show_frame("PlayerTurn")


class PlayerTurn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.gesture_to_method = {'left and right': "stay", 'up and down': "hit", 'fist': "double"}

        # Dealer Card
        self.dealer_label_text = tk.StringVar()
        self.dealer_label_text.set('The dealer currently has a ' + ' face up')
        self.dealer_label = tk.Label(self, textvariable=self.dealer_label_text, font=controller.title_font)

        # Info tab
        self.info_label_text = tk.StringVar()
        self.info_label_text.set('')
        self.info_label = tk.Label(self, textvariable=self.info_label_text, font=controller.title_font)
        
        # Cards
        self.card_label_text = tk.StringVar()
        self.card_label_text.set(str(game.get_player_hand(0)))
        self.card_label = tk.Label(self, textvariable=self.card_label_text, font=controller.title_font)

        # Card label
        self.cards_label = tk.Label(self, text="Your Cards:")
        
        # Card total
        self.card_total_label = tk.Label(self, text="Your hand is valued at:")
        self.card_total_text = tk.IntVar()
        self.card_total_text.set(player_hand.get_total())
        self.total_label = tk.Label(self, textvariable=self.card_total_text, font=controller.title_font)

        # Buttons
        self.hit_button = tk.Button(self, text="Hit!", command=lambda: self.update("hit"))
        self.stay_button = tk.Button(self, text="Stay!", command=lambda: self.update("stay"))
        self.reset_button = tk.Button(self, text="Double Down!", command=lambda: self.update("double"))

        # PlayerTurn layout
        self.dealer_label.grid(row=0, column=0, sticky=tk.W)
        self.cards_label.grid(row=1, column=0, sticky=tk.W)
        self.card_label.grid(row=1, column=1, columnspan=2, sticky=tk.E)
        self.card_total_label.grid(row=2, column=0, sticky=tk.W)
        self.total_label.grid(row=2, column=1, columnspan=2, sticky=tk.E)
        self.hit_button.grid(row=4, column=0)
        self.stay_button.grid(row=4, column=1)
        self.reset_button.grid(row=4, column=2, sticky=tk.W+tk.E)

    # Updates the total
    def update(self, method):
        if method == "hit":
            game.player_hit(0)
        elif method == "stay":
            self.controller.show_frame("DealerTurn")
        elif method == "double":
            game.player_double_down(0)
            self.controller.show_frame("DealerTurn")

        current_total = player_hand.get_total()

        if current_total == 21:
            self.controller.show_frame("DealerTurn")
        elif current_total > 21:
            self.controller.show_frame("DealerTurn")

        self.card_label_text.set(str(player_hand))
        self.card_total_text.set(current_total)

    def show(self):
        self.dealer_label_text.set('The dealer currently has a ' + str(game.dealer[-1]) + ' face up')
        self.card_label_text.set(str(player_hand))
        self.card_total_text.set(player_hand.get_total())
        return self

    def play_turn(self):

        result = gesture_recognizer.look_for_gesture()
        method = self.gesture_to_method[result]

        if method == "hit":
            
            game.player_hit(0)
            current_total = player_hand.get_total()
            self.card_label_text.set(str(player_hand))
            self.card_total_text.set(current_total)
            
            if current_total >= 21:
                self.controller.show_frame("DealerTurn")

            return self.play_turn()

        if method == "stay":
            self.controller.show_frame("DealerTurn")
        elif method == "double":
            game.player_double_down(0)
            self.controller.show_frame("DealerTurn")






class DealerTurn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Dealer Card
        self.information_label_text = tk.StringVar()
        self.information_label_text.set('Dealer Turn...')
        self.information_label = tk.Label(self, textvariable=self.information_label_text, font=controller.title_font)
        
        # Cards
        self.card_label_text = tk.StringVar()
        self.card_label_text.set(str(game.get_player_hand(0)))
        self.card_label = tk.Label(self, textvariable=self.card_label_text, font=controller.title_font)

        # Card label
        self.cards_label = tk.Label(self, text="Dealer's Cards:")
        
        # Card total
        self.card_total_label = tk.Label(self, text="Dealer's hand is valued at:")
        self.card_total_text = tk.IntVar()
        self.card_total_text.set(game.dealer.get_total())
        self.total_label = tk.Label(self, textvariable=self.card_total_text, font=controller.title_font)

        # Buttons
        self.hit_button = tk.Button(self, text="Continue!", command=lambda: self.controller.show_frame('PayoutScreen'))

        # DealerTurn layout
        self.information_label.grid(row=0, column=0, sticky=tk.W)
        self.cards_label.grid(row=1, column=0, sticky=tk.W)
        self.card_label.grid(row=1, column=1, columnspan=2, sticky=tk.E)
        self.card_total_label.grid(row=2, column=0, sticky=tk.W)
        self.total_label.grid(row=2, column=1, columnspan=2, sticky=tk.E)

        self.TimerInterval = 3000
        self.round = 0
        #self.dealer_turn()

    def show(self):
        self.information_label_text.set('Dealer Turn...')
        self.card_label_text.set(str(game.dealer))
        self.card_total_text.set(game.dealer.get_total())
        return self

    def dealer_turn(self):
        if self.round == 0:
            self.hit_button.grid_forget()
            self.round += 1
            self.after(1250, self.dealer_turn)
        elif game.dealer.get_total() < 17:
            game.dealer.add_card(game.deck.draw_card())
            self.card_label_text.set(str(game.dealer))
            self.information_label_text.set('Dealer Turn...Dealer just drew a ' + str(game.dealer[-1]))
            self.card_total_text.set(game.dealer.get_total())
            self.after(self.TimerInterval,self.dealer_turn)
        else:
            self.information_label_text.set('The dealer ends their turn with a score of ' + str(game.dealer.get_total()))
            self.hit_button.grid(row=4, column=0)
            self.round = 0
            gesture_recognizer.wait_for_fist()
            self.controller.show_frame('PayoutScreen')
        

class PayoutScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Information Panel
        self.information_label_text = tk.StringVar()
        self.information_label_text.set('Time to tally up the bet...')
        self.information_label = tk.Label(self, textvariable=self.information_label_text, font=controller.title_font)
        
        # Your score
        self.your_score_text = tk.StringVar()
        self.your_score_text.set('You finished your turn with a score of ' + str(player_hand.get_total()))
        self.your_score_label = tk.Label(self, textvariable=self.your_score_text, font=controller.title_font)
        
        # Dealer score 
        self.dealer_score_text = tk.StringVar()
        self.dealer_score_text.set('The dealer finished their turn with a score of ' + str(game.dealer.get_total()))
        self.dealer_score_label = tk.Label(self, textvariable=self.dealer_score_text, font=controller.title_font)

        # Result Panel
        self.result_label_text = tk.StringVar()
        self.result_label_text.set('')
        self.result_label = tk.Label(self, textvariable=self.result_label_text, font=controller.title_font)

        # Buttons
        self.continue_button = tk.Button(self, text="Continue!", command=lambda: self.controller.show_frame('BettingPage'))

        # DealerTurn layout
        self.information_label.pack()
        self.your_score_label.pack()
        self.dealer_score_label.pack()
        self.result_label.pack()
        self.continue_button.pack()

        self.step = 0
        #self.dealer_turn()

    def show(self):
        self.your_score_label.pack_forget()
        self.dealer_score_label.pack_forget()
        self.continue_button.pack_forget()
        self.result_label.pack_forget()
        self.your_score_text.set('You finished your turn with a score of ' + str(player_hand.get_total()))
        self.dealer_score_text.set('The dealer finished their turn with a score of ' + str(game.dealer.get_total()))
        return self

    def payout(self):
        if self.step == 0:
            self.your_score_label.pack()
            self.step += 1
            self.after(1250, self.payout)
        elif self.step == 1:
            self.dealer_score_label.pack()
            self.step += 1
            self.after(1250,self.payout)
        elif self.step == 2:
            result = ''
            if player_hand.get_total() > 21:
                result = 'You busted...You lose your bet of ' + str(player_wallet.get_last_bet())
            elif game.dealer.get_total() > 21:
                result = 'Dealer busted...You get your bet of ' + str(player_wallet.get_last_bet()) + ' back'
                player_wallet.return_bet()
            elif player_hand.get_total() > game.dealer.get_total():
                result = 'You beat the dealer!!! You receive ' + str(int(player_wallet.get_last_bet()*1.5)) + ' coins!'
                game.pay_out(0)
            elif player_hand.get_total() < game.dealer.get_total():
                result = 'The dealer beat you...Your lose your bet of ' + str(player_wallet.get_last_bet())
            else:
                result = 'You tied with the dealer...You receive your bet of ' + str(player_wallet.get_last_bet()) + ' back'          
            self.result_label_text.set(result)
            self.result_label.pack()
            self.continue_button.pack()
            self.step += 1
            self.after(500,self.payout)
        elif self.step == 3:
            gesture_recognizer.wait_for_fist()
            self.step = 0
            self.controller.show_frame('BettingPage')

if __name__ == "__main__":
    app = BlackJackGUI()
    app.mainloop()

