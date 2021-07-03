# *****************************************************************************************************************
#
# War Card Game v1.0
# Written by, Clifford A. Chipman
# Friday, July 2, 2021
#
# *****************************************************************************************************************
#
#       Import modules
#
# *****************************************************************************************************************
#
from datetime import datetime, timedelta
import random
import math
#
# *****************************************************************************************************************
#
gameStartedAt = datetime.now()  # Record the time the game began for statistics report
#
humanWar = []                   # Keeps track of the human's cards during war
computerWar = []                # Keeps track of the computer's cards during war
sequentialDeck = []             # A list of sequential playing cards
randomSequence = []             # A random sequence of integers from 1 to 52 used to generate the shuffled deck
shuffledDeck = []               # A shuffled list of playing cards generated from the sequential deck and the random sequence lists
humanHand = []                  # A list of playing cards dealt to the human player from the shuffled deck
computerHand = []               # A list of playing cards dealt to the computer player from the shuffled deck
#
endTheGame = False              # Trips a warning flag to immediately end the game because one player does not have enough cards to finish
#
roundNumber = 0                 # Keeps track of how many rounds have been played
minHumanCards = 52              # Keeps track of minimum number of human cards for game statistics
minComputerCards = 52           # Keeps track of minimum number of computer cards for game statistics
warOccurs = 0                   # Keeps track of the number of times WAR occurs
#
stars = '****************************************'
#
winner = ()                     # tuple returned by whoWins() function
                                # winner[0] Who wins a round: 'human', 'computer', or 'war'
                                # winner[1] How many additional times did war occur?
                                # winner[2] Sets or resets endTheGame flag
#
suits = ('Spades', 'Hearts', 'Clubs', 'Diamonds')
#
# cards tuple begin with 'Null' so card number & tuple index match to avoid confusion when reading the code
cards = ('Null', 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', 'Ten', 'Jack', 'Queen', 'King')
#
cardValues = {                  # This is a dictionary of playing cards' assigned values to determine who wins a round.
	cards[0] :0,  # Null
	cards[1] :14, # Ace
	cards[2] :2,  # 2
	cards[3] :3,  # 3
	cards[4] :4,  # 4
	cards[5] :5,  # 5
	cards[6] :6,  # 6
	cards[7] :7,  # 7
	cards[8] :8,  # 8
	cards[9] :9,  # 9
	cards[10]:10, # Ten
	cards[11]:11, # Jack
	cards[12]:12, # Queen
	cards[13]:13  # King
	}
#
# Returns the integer value of a particular playing card by looking it up in the cardValues dictionary
def valueOfCard(card):
    return cardValues[card[0:card.index(' of ')]]
#
# Returns a variable length string of spaces based on the length of a parameter string
def tabStop(card):
    return ' ' * (20 - len(card))
#
# Compares the two values of the human's card and the computer's card and determines the winner or declares war
def whoWins(humanCard,computerCard):
    additionalWars = 0
    if valueOfCard(humanCard) > valueOfCard(computerCard):
        print(f"\nHuman takes Computer's {computerCard}")
        if len(humanWar) > 0 or len(computerWar) > 0:
            for card in humanWar:                   # Add contents of human's War cards to human's hand
                humanHand.append(card)
            humanWar.clear()                        # Clear human's War cards
            for card in computerWar:                # Add contents of computer's War cards to human's hand
                humanHand.append(card)
            computerWar.clear()                     # Clear computer's War cards
        else:
            humanHand.append(computerCard)          # Add loser's card to winner's hand
            humanHand.append(humanCard)             # Place winner's card at end of winner's hand
            humanHand.pop(0)                        # Remove winner's card from place at top of winner's hand
            try:
                computerHand.remove(computerCard)   # Remove loser's card from loser's hand
            except:
                pass                                # No big deal if it was already done - just keep moving
        return ('human',additionalWars, False)      # Declare the winner, update additional wars, endTheGame = False
#
    elif valueOfCard(humanCard) < valueOfCard(computerCard):
        print(f"\nComputer takes Human's {humanCard}")
        if len(humanWar) > 0 or len(computerWar) > 0:
            for card in humanWar:                   # Add contents of human's War cards to computer's hand
                computerHand.append(card)
            humanWar.clear()                        # Clear human's War cards
            for card in computerWar:                # Add contents of computer's War cards to computer's hand
                computerHand.append(card)
            computerWar.clear()                     # Clear computer's War cards
        else:
            computerHand.append(humanCard)          # Add loser's card to winner's hand
            computerHand.append(computerCard)       # Place winner's card at end of winner's hand
            computerHand.pop(0)                     # Remove winner's card from place at top of winner's hand
            try:
                humanHand.remove(humanCard)         # Remove loser's card from loser's hand
            except:
                pass                                # No big deal if it was already done - just keep moving
        return ('computer', additionalWars, False)  # Declare the winner, update additional wars, endTheGame = False
#
    else:
        print("\n\t***** !!!WAR!!! *****")          # Declare war
        results = warRoutine()
        additionalWars += 1                         # Update game statistics
        return (results[0], additionalWars, results[1])
#
def warRoutine():
#
# This happens when the two exposed playing cards are equal
#
# Each player deals three cards face down and a 4th card face up from their hand
# The 4th card determines the winner
#
# First, make sure both players' hands have enough cards for a WAR routine
    if len(humanHand) > 3 and len(computerHand) > 3:
        print("  Human's Cards       Computer's Cards")
        for i in range(0,4):                        # Deal four cards from each player's hand [0-3]
            if i < 3:
                # The first three (i = 0 - 2) are face down -- ** MYSTERY CARD **
                print(f"** MYSTERY CARD **{tabStop('** MYSTERY CARD **')}** MYSTERY CARD **")
            else:
                # Now display the fourth (i = 3) face up
                print(f"{humanHand[0]}{tabStop(humanHand[0])}{computerHand[0]}")
            humanWar.append(humanHand[0])           # Add player's card to their war list
            humanHand.pop(0)                        # Remove player's card from the top of their hand list
            computerWar.append(computerHand[0])     # Add computer's card to their war list
            computerHand.pop(0)                     # Remove computer's card from the top of their hand list
#
        results = whoWins(humanWar[-1],computerWar[-1]) # Use the last cards in the lists to determine the winner
                                                        # THIS TAKES ADDITIONAL WARS INTO ACCOUNT!!!
        return (results[0], False)                  # Return whoever wins & reset endOfGame flag
#
    else: # One of the players do NOT have enough cards for a WAR routine...
        if len(humanHand) < 4:
            # winner = 'computer'
            if len(humanHand) == 1:                 # Display singular "card"
                print(f"\nYou only have {len(humanHand)} card.")
            else:                                   # Display plural "cards"
                print(f"\nYou only have {len(humanHand)} cards.")
            # endTheGame = True
            return ('computer', True)               # Return 'computer' as winner & set endOfGame flag
        else: # len(computerHand) < 4:
            # winner = 'human'
            print(f"\nThe computer only has {len(computerHand)} cards.")
            # endTheGame = True
            return ('human', True)                  # Return 'human' as winner & set endOfGame flag
#
def exitToOperatingSystem():                        # Generate a report of game statistics & append gameEndedAt stat
    currentGameStatsReport()
    print(f"Game Ended At:\t\t\t{gameEndedAt.isoformat()}")
    return
#
def currentGameStatsReport():                       # Generate a report of game statistics
    print(f"Number of Completed Rounds:\t{roundNumber}")
    print(f"Smallest Human Deck:\t\t{minHumanCards} cards")
    print(f"Smallest Computer Deck: \t{minComputerCards} cards")
    print(f"War Occurred:\t\t\t{warOccurs} times")
    print(f"Game Started At:\t\t{gameStartedAt.isoformat()}")
    print(f"Game Duration:\t\t\t{str(gameDuration)}")
#
# future stats:
#
    return
#
# *****************************************************************************************************************
#
# Title Screen
#
# *****************************************************************************************************************
#
print(f"{stars}")
print("\nWar Card Game v1.0")
print("Written by, Clifford A. Chipman")
print("Friday, July 2, 2021")
#
# *****************************************************************************************************************
#
# Initialize the game
#
# *****************************************************************************************************************
#
# Build a sequential deck from cards & suits
print(f"\n{stars}")
print("\nOpening a new deck of cards...")
sequentialDeck.append('Null')
for suit in suits:
    for card in cards:
        if card == 'Null':
            continue
        sequentialDeck.append(card + ' of ' + suit)
#
#Uncomment to debug
#print("Sequential Deck:")
#for card in sequentialDeck:
#    print(card)
#############################
#
# Shuffle the deck by generating a random sequence from the integers 1 - 52
print("Shuffling the deck...")
for card in sequentialDeck:
    if card == 'Null':
        continue
    r = random.randint(1,52)
    while r in randomSequence:
        r = random.randint(1,52) # get another number if r already exists in randomSequence
    randomSequence.append(r)
#
#Uncomment to debug
#print("Random Sequence:")
#print(randomSequence)
#############################
#
# Assign a card from sequential deck to a position in shuffled deck based on random sequence list
shuffledDeck.append('Null')
for n in randomSequence:
    shuffledDeck.append(sequentialDeck[n])
#
#Uncomment to debug
#print("Shuffled Deck:")
#for card in shuffledDeck:
#    print(card)
#############################
#
# Deal the cards
print("Dealing the cards...")
#
deckIdx = 1
while deckIdx < len(shuffledDeck):
    if math.fmod(deckIdx,2) == 0:
        computerHand.append(shuffledDeck[deckIdx]) # Computer gets even cards
        #humanHand.append(shuffledDeck[deckIdx])    # Human gets even cards
    else:
        humanHand.append(shuffledDeck[deckIdx])    # Human gets odd cards
        #computerHand.append(shuffledDeck[deckIdx]) # Computer gets odd cards
    deckIdx += 1
#
#Uncomment to debug
#print(f"\nHuman's hand: {len(humanHand)} cards")
#for card in humanHand:
#    print(card)
##################################################
#
#Uncomment to debug
#print(f"\nComputer's hand: {len(computerHand)} cards")
#for card in computerHand:
#    print(card)
#
#Uncomment to debug
#print(" Human's Hand        Computer's Hand")
#for card in range(1,26):
#    if valueOfCard(humanHand[card]) > valueOfCard(computerHand[card]):
#        winMsg = 'Human'
#    elif valueOfCard(humanHand[card]) < valueOfCard(computerHand[card]):
#        winMsg = 'Computer'
#    else:
#        winMsg = '*** WAR!!! ***'
#    print(f"{humanHand[card]}{tabStop(humanHand[card])}{computerHand[card]}{tabStop(computerHand[card])}{winMsg}")
#####################################################################################################################
#
# Play until one players' hand is empty or one player does not have enough cards for a WAR
while len(humanHand) > 0 and len(computerHand) > 0 and (not endTheGame):
#
    validInput = False
    while not validInput:
        print(f"\n{stars}")
        print(f"\nYour deck has {len(humanHand)} cards")
        if len(humanHand) < minHumanCards: minHumanCards = len(humanHand)               # update game statistics
        if len(computerHand) < minComputerCards: minComputerCards = len(computerHand)   # update game statistics
        print(f"Computer's deck has {len(computerHand)} cards")
#
# Uncomment to debug:
#        print(f"Total cards: {len(humanHand) + len(computerHand)} cards")
#
        print("\nPeek at [H]uman's deck (YOU CHEATER!!!)")
        print("Peek at [C]omputer's deck (YOU CHEATER!!!)")
        print("Display Current Game [S]tatistics Report")
        print("[P]lay round")
        print("[Q]uit")
#
        userInput = input(f"\nCompleted Rounds: {roundNumber} | Select an option:> ")
        userInput = userInput.upper()                   # Capitalize it and...
        if len(userInput) > 1: userInput = userInput[0] # ...take only the first character
#
        if userInput == 'H': # User wants to cheat
            print("\nHere are the contents of your deck YOU CHEATER!!!")
            for card in humanHand:
                print(card)
            # validInput is still False, so execution will remain within validInput while loop

#
        elif userInput == 'C': # User wants to cheat
            print("\nHere are the contents of Computer's deck YOU CHEATER!!!")
            for card in computerHand:
                print(card)
            # validInput is still False, so execution will remain within validInput while loop
#
        elif userInput == 'S': # User requests a game statistics report
            gameDuration = datetime.now() - gameStartedAt
            currentGameStatsReport()
            # validInput is still False, so execution will remain within validInput while loop
            
        elif userInput == 'Q': # User gives up, so insult them & exit to operating system immediately
            print(f"\nYOU QUITTER!!!\n")
            gameEndedAt = datetime.now()                # update game statistics
            gameDuration = gameEndedAt - gameStartedAt  # update game statistics
            exitToOperatingSystem()
            exit(0)
#
        elif userInput == 'P':
            validInput = True # User wants to play a round, so leave the while loop & play a round
#
        else:
            pass # validInput is still False, so execution will remain within while loop
#
    print(f"\nYour top card is: {humanHand[0]}")        # Expose human's top card
    print(f"Computer's top card is: {computerHand[0]}") # Expose computer's top card
    winner = whoWins(humanHand[0],computerHand[0])
    roundNumber += 1                                    # Count another round
    warOccurs += winner[1]                              # update game statistics
    endTheGame = winner[2]                              # update endTheGame flag
#
# Uncomment to debug
#    print(f"End The Game Flag: {endTheGame}")
#
# At this point, either one of the players has an empty hand or not enough cards to finish a WAR routine:
#
# So, declare the winner!!!
if winner[0] == 'computer': print("Computer wins!\n")
if winner[0] == 'human': print("You win!\n")
#
# and end the game...
gameEndedAt = datetime.now()
gameDuration = gameEndedAt - gameStartedAt
exitToOperatingSystem()
exit(0)
