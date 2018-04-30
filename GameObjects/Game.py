################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################
from Deck import Deck
from Hand import Hand
from Wallet import Wallet

class Game(object):

    def __init__(self, num_players=1, minimum_bet=500):
        """Constructor"""

        self.deck = Deck()
        self.dealer = Hand()
        self.players = []
        self.minimum_bet = minimum_bet

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


    def reshuffle_deck(self):
        """Reshuffles the deck"""

        self.deck.reshuffle()


    def clear_hands(self):
        """Clears the dealer and all players' cards from their hand"""

        # Clear dealer
        self.dealer.clear_hand()

        # Clear each player
        for player in self.players:

            player_hand = player[0]
            player_wallet = player[1]

            player_hand.clear_hand()


    def player_hit(self, player_id):
        """Gives the given player an additional card"""

        player = self.players[player_id]

        player_hand = player[0]
        player_hand.add_card(self.deck.draw_card())


    def play_dealers_turn(self):
        """Plays out the dealers turn"""
        pass


    def place_bet(self, player_id, amount):
        """Takes out a bet for the given player, returns whether or not the
        bet is possible"""

        player = self.players[player_id]

        player_wallet = player[1]
        
        return player_wallet.place_bet(amount)


    def can_player_double_down(self, player_id):
        """Checks if a player can legally double down"""

        player = self.players[player_id]
        player_hand = player[0]
        player_wallet = player[1]
        last_bet = player_wallet.get_last_bet()

        # PLayer must have enough money in their wallet
        if player_wallet.amount() - last_bet >= 0:
            return True

        return False


    def player_double_down(self, player_id):
        """When a player doubles down, they double their bet in exchange for
        exactly one more card. If they win, they get twice as much money. 
        Returns the new card"""

        player = self.players[player_id]
        player_hand = player[0]
        player_wallet = player[1]
        player_wallet.double_down()
        self.player_hit(player_id)
        return player_hand[-1]



    def pay_out(self, player_id):
        """Pays the given player 1.5 times their last bet"""

        player = self.players[i]
        player_wallet = player[1]
        players_bet = player_wallet.get_last_bet()
        payout = int(players_bet * 1.5)
        player_wallet.add_money(payout)


    def get_player_money(self, player_id):
        """Returns how much the given player has in their wallet"""

        return self.players[player_id][1].amount()


    def get_player_hand(self, player_id):
        """Returns the given player's hand"""

        return self.players[player_id][0]


