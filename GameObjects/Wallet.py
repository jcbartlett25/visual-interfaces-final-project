################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################


class Wallet(object):
    """The wallet represents the amount of money a player currently has"""

    def __init__(self, amount=5000):
        """Constructor"""

        self._money = amount

    
    def place_bet(self, amount):
        """Removes a given amount of money from the wallet, returns True or False
        depending on whether or not there was enough money in the wallet to
        complete the bet"""

        self._money -= amount

        if self._money >= 0:
            return True
        else:
            return False


    def add_money(self, amount):
        """Adds the given amount of money to the wallet"""

        self._money += amount


    def amount(self):
        """Returns the amount of money currently in the wallet"""

        return self._money


    # Python object functions to make code cleaner
    def __str__(self):
        return "Wallet(" + str(self._money) + ")"
    def __repr__(self):
        return "Wallet(" + str(self._money) + ")"