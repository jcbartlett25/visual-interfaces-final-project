from Card import Card
from collections import deque
import random

class Deck(object):
    """A deck is a collection of cards"""

    # Private values for the deck
    _VALUES = (1,2,3,4,5,6,7,8,9,10,11,12,13)
    _SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
    _cards = deque()

    def __init__(self):
        """Constructor"""

        # Create the standard six set deck
        for i in range(0, 6):
            for suit in self._SUITS:
                for value in self._VALUES:
                    self._cards.append(Card(suit, value))

        # Shuffle the cards
        random.shuffle(self._cards)


    def reshuffle(self):
        """Reshuffles the cards so we have a full 6-set deck again"""

        # Clear out the current cards
        self._cards.clear()

        # Recreate the standard six set deck
        for i in range(0, 6):
            for suit in self._SUITS:
                for value in self._VALUES:
                    self._cards.append(Card(suit, value))

        # Shuffle the cards
        random.shuffle(self._cards)


    def draw_card(self):
        """Returns the top card and removes it from the deck"""
        return self._cards.pop()


    def total_cards(self):
        """Returns the total number of cards in the deck currently"""
        return len(self._cards)

        