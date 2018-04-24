################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################


class Card(object):
    """Container for a card object"""

    def __init__(self, suit, value):
        """Constructor"""

        self.suit = suit
        self.value = value


    def display_name(self):
        """Returns the display name of a card"""

        if self.value == 1:
            return 'Ace of ' + self.suit
        elif self.value == 11:
            return 'Jack of ' + self.suit
        elif self.value == 12:
            return 'Queen of ' + self.suit
        elif self.value == 13:
            return 'King of ' + self.suit
        else:
            return str(self.value) + ' of ' + self.suit


    # Python object functions to make code cleaner
    def __repr__(self):
        return self.display_name()
    def __str__(self):
        return self.display_name()
    def __hash__(self):
        return hash(self.display_name())