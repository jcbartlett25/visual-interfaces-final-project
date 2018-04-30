################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################


class Hand(object):
    """A hand represents the cards currently in a player's hand"""

    _VALUE_TABLE = {
    1: 11,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 10,
    12: 10,
    13: 10
    }

    _soft_aces = 0
    _total = 0

    def __init__(self):
        """Constructor"""

        self._cards = []


    def add_card(self, card):
        """Adds a card to the current hand"""
        
        self._cards.append(card)
        
        # Keep track of the aces
        if card.value == 1:
            self._soft_aces += 1
        
        # Keep track of the total
        self._total += self._VALUE_TABLE[card.value]


    def get_total(self):
        """Gets the total value for this hand"""

        # If there's a soft ace and the hand is worth more than 21 points
        if self.is_soft_hand() and self._total > 21:
            self._total -= 10
            self._soft_aces -= 1

        return self._total

    def clear_hand(self):
        """Removes all of the cards currently in this hand"""

        # Clear everything
        del self._cards[:]
        self._soft_aces = 0
        self._total = 0


    def show_hand(self):
        """Shows all the cards currently in this hand"""

        return str(self._cards)


    def is_soft_hand(self):
        """Determines if this hand has an ace card worth 11 points"""

        if self._soft_aces > 0:
            return True
        else:
            return False


    # Python object functions to make code cleaner
    def __repr__(self):
        return self.show_hand()
    def __str__(self):
        return self.show_hand()
    def __getitem__(self, i): 
        return self._cards[int(i)]