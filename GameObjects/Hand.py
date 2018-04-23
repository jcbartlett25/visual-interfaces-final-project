class Hand(object):
    """A hand represents the cards currently in a player's hand"""

    def __init__(self):
        """Constructor"""

        self._cards = []


    def add_card(self, card):
        """Adds a card to the current hand"""
        
        self._cards.append(card)


    def get_total(self):
        """Gets the total value for this hand"""

        total = 0

        for card in self._cards:
            total += card.value

        return total

    def clear_hand(self):
        """Removes all of the cards currently in this hand"""

        self._cards.clear()


    def show_hand(self):
        """Shows all the cards currently in this hand"""

        return str(self._cards)


    # Used while testing the class
    def __repr__(self):
        return self.show_hand()
    def __str__(self):
        return self.show_hand()