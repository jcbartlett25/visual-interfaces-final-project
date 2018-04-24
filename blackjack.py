################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################
from GameObjects.Game import Game

# Welcome message, gather number of users
print('Welcome to BlackJack!')
num_players = raw_input('How many players do you want to play with? ')
num_players = int(num_players)

# Checking to see if number of players is valid
if num_players <= 0:
    print('Too few players...')
    exit(0)
elif num_players >= 5:
    print('Too many players...Please choose a number between 1 and 4')
    exit(0)

print('Awesome...Starting Game with ' + str(num_players) + ' player(s)')

game = Game(num_players=num_players)
