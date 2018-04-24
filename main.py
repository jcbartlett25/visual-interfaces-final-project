################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################
from GameObjects.Deck import Deck
from GameObjects.Hand import Hand
from GameObjects.Wallet import Wallet
from GameObjects.Game import Game

game = Game(num_players=2)

game.deal_cards()
game.deal_cards()

print(game.players[0])
