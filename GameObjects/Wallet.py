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
        self._last_bet = 0

    
    def place_bet(self, amount):
        """Removes a given amount of money from the wallet, returns True or False
        depending on whether or not there was enough money in the wallet to
        complete the bet"""

        if self._money < amount:
            return False
        
        self._money -= amount
        self._last_bet = amount
        return True


    def add_money(self, amount):
        """Adds the given amount of money to the wallet"""

        self._money += amount


    def return_bet(self):
        """Gives a player back their bet"""

        self._money += self._last_bet


    def amount(self):
        """Returns the amount of money currently in the wallet"""

        return self._money


    def get_last_bet(self):
        """Returns the amount of money that was taken out in the last bet"""

        return self._last_bet


    def double_down(self):
        """Takes out an additional bet and sets the last bet to twice as much"""

        can_pay = self.place_bet(self._last_bet)
        
        if can_pay:
            self._last_bet *= 2

        return can_pay


    # Python object functions to make code cleaner
    def __str__(self):
        return "Wallet(" + str(self._money) + ")"
    def __repr__(self):
        return "Wallet(" + str(self._money) + ")"