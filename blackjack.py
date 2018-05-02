################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################
from GameObjects.Game import Game

KEEP_PLAYING = True
SHUFFLE_LIMIT = 60

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

# Create game object
game = Game(num_players=num_players)

# Give some basic rules
print('Each player begins with 5000 coins.\nThe default bet will be 500\n\n')
print('The game will now begin')

# Keep track of the number of rounds played
num_rounds = 1

# While there are still eligible players and the user wants to continue
while game.players and KEEP_PLAYING:

    print('Round '+str(num_rounds)+'...START!')

    # Reset everyone's hands
    game.clear_hands()

    # Reshuffle the deck when the limit is reached
    if len(game.deck) < SHUFFLE_LIMIT:
        print('Reshuffling cards...Done')
        game.reshuffle_deck()

    print('Place your bets...')
    for player_id, player in enumerate(game.players):

        valid_bet = False

        # Keep going until player makes a valid bet
        while not valid_bet:

            print('Player ' + str(player_id+1) + ' currently has ' + str(player[1].amount()) + ' coins')
            betting_amount = raw_input('Player ' + str(player_id+1) + ' how much would you like to bet? (Press enter for the minimum bet) ')

            # Default bet
            if betting_amount == '':
                betting_amount = 500

            # Make sure the value is an integer
            try:
                betting_amount = int(betting_amount)
            except ValueError:
                print('Please provide a valid number\n')
                continue

            # Make sure the bet amount is greater than or equal to minimum betting value
            if betting_amount < 500:
                print('Bet amount is less than the minimum bet...Please try again\n')
                continue

            # Make the bet, if the user doesn't have enough money, tell them
            if not game.place_bet(player_id, betting_amount):
                print('This player does not have enough money for this bet\n\n')
            else:
                print('Great!\n\n')
                valid_bet = True

    print('All bets are in! \nNow let\'s deal some cards...')
    
    # Deal everyone (including the dealer) in the game two cards to begin with
    game.deal_cards()
    game.deal_cards()

    print('The dealer currently has a ' + str(game.dealer[0]) + ' face up\n')

    # Check if dealer had blackjack
    dealer_score = game.dealer.get_total()
    if dealer_score == 21:
        print('Dealer has Blackjack!')
        for player_id, player in enumerate(game.players):
            if player[0].get_total() != 21:
                print('Sorry Player ' + str(player_id+1) + ', you lose your bet')
            else:
                print('Player ' + str(player_id+1) + ' also had blackjack and gets to keep their bet')
                player[1].return_bet()
        continue

    # Play each player's turn
    for player_id, player in enumerate(game.players):

        players_turn = True

        player_hand = player[0]
        player_wallet = player[1]

        print('Player ' + str(player_id+1) + '\'s Turn!')

        while players_turn:

            print('\nYour hand is currently: ' + str(player_hand))
            print('Your hand is valued at ' + str(player_hand.get_total()))
            choice = raw_input('Would you like to (H)it, (S)tay, or (D)ouble Down? ')

            if choice.lower() == 'h':
                print('HIT!')
                game.player_hit(player_id)
                print('Your new card is...' + str(player_hand[-1]))
                

            elif choice.lower() == 's':
                print('STAY!')

                # End the players turn
                players_turn = False
                

            elif choice.lower() == 'd':

                if game.can_player_double_down(player_id):

                    print('DOUBLE DOWN!')
                    game.player_double_down(player_id)
                    print('Your new card is...' + str(player_hand[-1]))

                    # End the players turn
                    players_turn = False

                # Player does not have sufficient money
                else:
                    print('You do not have enough money to double down...')

            
            current_total = player_hand.get_total()

            if current_total == 21:
                print('BLACKJACK!!!!!')

                # End the players turn
                players_turn = False

            elif current_total > 21:
                print('BUST!!')

                # End the players turn
                players_turn = False

        print('You end your turn with a value of ' + str(player_hand.get_total()) + '\n\n')

    # Play out the dealer's turn
    print('The dealer currently has: ' + str(game.dealer))
    print('Their hand is worth ' + str(game.dealer.get_total()))
    while game.dealer.get_total() < 17:
        game.dealer.add_card(game.deck.draw_card())
        print('The dealer now draws a...'+ str(game.dealer[-1]))
        print('The dealer currently has: ' + str(game.dealer))
        print('Their hand is worth ' + str(game.dealer.get_total()))
    print('The dealer ends their turn with a value of ' + str(game.dealer.get_total()))
    print('\n\nTime to tally up the bets!')

    dealer_score = game.dealer.get_total()

    # Look at each player and give out money if necessary
    for player_id, player in enumerate(game.players):

        player_hand = player[0]
        player_wallet = player[1]
        player_score = player_hand.get_total()

        if dealer_score > 21 and player_score <= 21:
            print('Dealer busted...Player ' + str(player_id+1) + ' gets their bet back')
            player_wallet.return_bet()
        elif player_score > 21:
            print('Player ' + str(player_id+1) + ' busted...You lose your bet')
        elif player_score > dealer_score:
            print('Player ' + str(player_id+1) + ' beat the dealer...')
            print('You will receive ' + str(int(player_wallet.get_last_bet()*1.5)) + ' coins')
            game.pay_out(player_id)
        elif player_score == dealer_score:
            print('Player ' + str(player_id+1) + ' has tied with the dealer...You will receive your bet back')
            player_wallet.return_bet()
        elif player_score < dealer_score:
            print('Player ' + str(player_id+1) + ' lost to the dealer...You lose your bet')
        else:
            print('idk whaddup witchu')


    # Ask user if they want to keep going at the end of each round
    answer = raw_input('Would you like to keep playing? (y/n) (Press enter to keep playing) ')

    # Default is yes
    if answer == '' or answer.lower() == 'y':
        print('Awesome!')
        num_rounds += 1
        continue
    else:
        print('Awww see ya next time!')
        KEEP_PLAYING = False

# Exit message
print('Thanks for playing!')