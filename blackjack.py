# *****************************************************************************************************************
#
# Blackjack Card Game v1.0
# Written by, Clifford A. Chipman
# Wednesday, September 1, 2021
#
# *****************************************************************************************************************
#
# Blackjack Rules
# https://www.kaggle.com/alexisbcook/blackjack-microchallenge
#
# We'll use a slightly simplified version of blackjack (aka twenty-one). In this version, there is one player 
# (who you'll control) and a dealer. Play proceeds as follows:
#
# - The player is dealt two face-up cards. The dealer is dealt one face-up card.
# - The player may ask to be dealt another card ('hit') as many times as they wish. If the sum of their cards 
#   exceeds 21, they lose the round immediately.
# - The dealer then deals additional cards to himself until either:
#     - The sum of the dealer's cards exceeds 21, in which case the player wins the round, or
#     - The sum of the dealer's cards is greater than or equal to 17. If the player's total is greater than the 
#       dealer's, the player wins. Otherwise, the dealer wins (even in case of a tie).
#
# When calculating the sum of cards, Jack, Queen, and King count for 10. Aces can count as 1 or 11. (When 
# referring to a player's "total" above, we mean the largest total that can be made without exceeding 21. 
# So A+8 = 19, A+8+8 = 17.)
#
# *****************************************************************************************************************
#
#       Import modules
#
# *****************************************************************************************************************
#
import random
import math
#
# *****************************************************************************************************************
#
scores = []
shuffledDeck = []               # A shuffled list of playing cards generated from the sequential deck and the random sequence lists
humanHand = []                  # A list of playing cards dealt to the human player from the shuffled deck
computerHand = []               # A list of playing cards dealt to the computer player from the shuffled deck
humanHandValue = 0              # Value of cards in human's hand
computerHandValue = 0           # Value of cards in computer's hand
numAces = 0                     # Quantity of Aces in player's hand
playerLost = False              # Flags if player score exceeds 21
dealersTurn = False             # Flags if player is satisfied with their hand
#
stars = '****************************************'
#
suits = ('Spades', 'Hearts', 'Clubs', 'Diamonds')
#
# cards tuple begin with 'Null' so card number & tuple index match to avoid confusion when reading the code
cards = ('Null', 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', 'Ten', 'Jack', 'Queen', 'King')
#
cardValues = {                  # This is a dictionary of playing cards' assigned values to determine who wins a round.
	cards[0] :0,  # Null
	cards[1] :11, # Ace
	cards[2] :2,  # 2
	cards[3] :3,  # 3
	cards[4] :4,  # 4
	cards[5] :5,  # 5
	cards[6] :6,  # 6
	cards[7] :7,  # 7
	cards[8] :8,  # 8
	cards[9] :9,  # 9
	cards[10]:10, # Ten
	cards[11]:10, # Jack
	cards[12]:10, # Queen
	cards[13]:10  # King
	}
#
def should_hit(player_total, dealer_card_val, player_aces):
    """Return True if the player should hit (request another card) given the current game
    state, or False if the player should stay. player_aces is the number of aces the player has.
    """
    return False
#
# Returns the integer value of a particular playing card by looking it up in the cardValues dictionary
def valueOfCard(card):
    return cardValues[card[0:card.index(' of ')]]
#
def handValue(hand):
    value = 0
    for card in hand:
        if valueOfCard(card) == 11: # card is an Ace
            if value + valueOfCard(card) > 21: # Check if using value of 11 would lose the game
                value += 1  # Assign Ace value of 1
            else:
                value += 11 # Assign Ace value of 11
        else:
            value += valueOfCard(card)
    return value
#
def shuffleDeck():
# First build a sequential deck from cards & suits
    print(f"\n{stars}")
    print("\nOpening a new deck of cards...")
    shuffled = []                   # A list of shuffled playing cards
    sequentialDeck = []             # A list of sequential playing cards
    randomSequence = []             # A random sequence of integers from 1 to 52 used to generate the shuffled deck
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
    shuffled.append('Null')
    for n in randomSequence:
        shuffled.append(sequentialDeck[n])
#
#Uncomment to debug
#print("Shuffled Deck:")
#for card in shuffledDeck:
#    print(card)
#############################

    return shuffled
#
def showHands():
    print(f"\n{stars}\n")
    print(f"Your hand: {handValue(humanHand)}")
    print(f"{humanHand}")
    if playerLost or dealersTurn:
        print(f"\nDealer's hand: {handValue(computerHand)}")
        print(f"{computerHand}")
    else:
        print(f"\nDealer's hand: ") #{handValue(computerHand)}")
        print(f"{computerHand[0]}")
    return [handValue(humanHand),handValue(computerHand)]
#
shuffledDeck = shuffleDeck()
#
#print(f"{len(shuffledDeck)} cards: ")
#print(shuffledDeck)
#
# - The player is dealt two face-up cards. The dealer is dealt one face-up card.
# - The player may ask to be dealt another card ('hit') as many times as they wish. If the sum of their cards 
#   exceeds 21, they lose the round immediately.
# - The dealer then deals additional cards to himself until either:
#     - The sum of the dealer's cards exceeds 21, in which case the player wins the round, or
#     - The sum of the dealer's cards is greater than or equal to 17. If the player's total is greater than the 
#       dealer's, the player wins. Otherwise, the dealer wins (even in case of a tie).
#
# Deal the cards
print("Dealing the cards...")
#
# Deal initial cards
for deckIdx in range(1,5):
    if math.fmod(deckIdx,2) == 0:
        computerHand.append(shuffledDeck[deckIdx]) # Computer gets even cards
        #humanHand.append(shuffledDeck[deckIdx])    # Human gets even cards
    else:
        humanHand.append(shuffledDeck[deckIdx])    # Human gets odd cards
        #computerHand.append(shuffledDeck[deckIdx]) # Computer gets odd cards
#
userInput = "H"
while userInput == "H":
    deckIdx += 1
#    print(f"Next Card #{deckIdx}")
    scores = showHands()
    if scores[0] > 21: # If the player loses, break out of this while loop
        playerLost = True
        break
    validInput = False
    while not validInput:
        userInput = input("\n[H]it or [S]tay: ")
        userInput = userInput.upper()   # Capitalize it and ...
        if len(userInput) > 1 :
            userInput = userInput[0]    # Take only the first character
        if userInput == "S" or userInput == "H":
            validInput = True
#
    if userInput == "H":
        humanHand.append(shuffledDeck[deckIdx])
#
# Did the player already lose? (scores[0] > 21)
if playerLost: 
    #
    exit("Player Lost")
#
print("\nDealer's turn")
dealersTurn = True
#
# - The dealer then deals additional cards to himself until either:
#     - The sum of the dealer's cards exceeds 21, in which case the player wins the round, or
#     - The sum of the dealer's cards is greater than or equal to 17. If the player's total is greater than the 
#       dealer's, the player wins. Otherwise, the dealer wins (even in case of a tie).
#
if scores[0] > 17:
    targetScore = scores[0] # Try to match the player's score
else:
    targetScore = 17
#
scores = showHands()
while scores[1] < targetScore:
    computerHand.append(shuffledDeck[deckIdx])
    deckIdx += 1
    scores = showHands()
#
if (scores[0] > scores[1]) or scores[1] > 21:
    exit("Player Wins!!!")
else:
    exit("Dealer Wins!!!")
#
