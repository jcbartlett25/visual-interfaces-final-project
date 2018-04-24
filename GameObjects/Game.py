################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################
from Deck import Deck
from Hand import Hand
from Wallet import Wallet

class Game(object):

    def __init__(self, num_players=1):
        """Constructor"""

        self.deck = Deck()
        self.dealer = Hand()
        self.players = []

        for i in range(0, num_players):
            self.players.append((Hand(), Wallet()))


    def deal_cards(self):
        """Deals out 1 card to the dealer and all players in the game"""

        # Draw a card from the deck and give it to the dealer
        self.dealer.add_card(self.deck.draw_card())

        # For each player, draw from the deck and add card
        for player in self.players:

            player_hand = player[0]
            player_wallet = player[1]

            player_hand.add_card(self.deck.draw_card())


    def clear_hands(self):
        """Clears the dealer and all players' cards from their hand"""

        # Clear dealer
        self.dealer.clear_hand()

        # Clear each player
        for player in self.players:

            player_hand = player[0]
            player_wallet = player[1]

            player_hand.clear_hand()


