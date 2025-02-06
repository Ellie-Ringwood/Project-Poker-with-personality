import random
from CardClass import Card
from DeckClass import Deck
from TableClass import Table
from PlayerClass import Player
        
## global functions
"""def getPreviousPlayerIndex(index):
    previousPlayer = index - 1
    if (previousPlayer < 0):
        previousPlayer = len(players) -1
    return previousPlayer"""

def betting(): ##returns is hand is won yet or not
    stillBetting = True
    i = 0
    while stillBetting:
        if (table.currentDifferenceInBets() != 0) or i == 0:
            for player in table.players:
                if (player.folded == False) and (table.continueBetting == True):
                    player.bet()
                if (table.continueBetting == False):
                    stillBetting == False
                    return False
        if (table.currentDifferenceInBets() == 0):
            stillBetting = False
        i += 1
    return True

def evaluateWinner():
    winnerIndexes = []

    for i in range(len(table.players)):
        if table.players[i].getCurrentCard().getValue() == table.getCommunityCard().getValue():
            winnerIndexes = [i]

    playerValues = []
    for i in range(len(table.players)):
        card = table.players[i].getCurrentCard().getValue()
        playerValues.append(card)

    for card in playerValues:
        if card == table.getCommunityCard().getValue():
            winnerIndexes = [i]
            return winnerIndexes

    maxValue = -1
    for i in range(len(playerValues)):
        if playerValues[i] > maxValue:
            winnerIndexes = [i]
            maxValue = playerValues[i]
        elif playerValues[i] == maxValue:
            winnerIndexes.append(i)
        
    return winnerIndexes

############################################ main code ############################################
##global attributes
global table
table = Table()
playing = True
hand = 0

# begin game
while playing:
    ## get list of players with funds
    table.getPlayersWithFunds()
    if (len(table.players) < 2):
        print("Not enough players with funds")
        playing = False
        break 

    for player in table.players:
        print(player.getName(),"has a balance of:", player.getBalance())

    ## begin hand
    hand += 1
    print("Hand",hand)
    roundOfPlay = 1
    handNotWon = True
    winner = -1
    deck = Deck()

    while handNotWon:
        if roundOfPlay == 1:
            if table.players:
                print("Round 1: Give blinds, get dealt a card, then bet")
                # remove blind amount from player funds
                for player in table.players: 
                    player.removeBlind()
                table.addCurrentBet(table.blindAmount)

                # shuffle and deal 1 card to each player
                deck.shuffleDeck()
                table.players[0].receiveCard(deck.dealCard())
                table.players[1].receiveCard(deck.dealCard())
                #for i in range(len(table.players)):
                #    table.players[i].receiveCard(deck.dealCard())

                # each player bets
                handNotWon = betting()
                
                roundOfPlay += 1
        elif (roundOfPlay == 2) and handNotWon == True:
            print("Round 2: Table gets dealt one community card, then bet")
            # shuffle and deal 1 community card to the table
            deck.shuffleDeck()
            table.recieveCommunityCard(deck.dealCard())
            ####then betting
            handNotWon = betting()
            roundOfPlay += 1
        elif (roundOfPlay > 2) and handNotWon == True:
            print("\nEvaluation")
            ####same value as public card wins
            ####if neither same, highest wins
            handNotWon = False
            
    print("End of hand")
    ####award money here
    if len(table.players)  == 1:
        #print("1 unfolded player left")
        table.endOfHand([0])
    else:
        #print("multiple unfolded players left")
        table.endOfHand(evaluateWinner())

    ## check still playing
    print("\npress e to exit, or anything else to continue:")
    exit = str(input("")).upper()
    if exit == "E":
        playing = False

print("End of game")