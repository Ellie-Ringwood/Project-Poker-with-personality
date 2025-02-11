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
playingHand = True

# begin game
while playingHand:
    ## get list of players with funds
    table.getPlayersWithFunds()
    if (len(table.players) < 2):
        print("Not enough players with funds")
        playingHand = False
        break 

    for player in table.players:
        print(player.getName(),"has a balance of:", player.getBalance())

    ## begin hand
    table.hand += 1
    print("\nHand",table.hand)
    
    deck = Deck()

    while table.handNotWon:
        if table.currentRound == 1:
            if table.players:
                print("Round 1: 1st player pays small blind (",table.blindAmount,"), second pays big blind (",table.blindAmount*2,"), get dealt a card, then bet")
                # remove blind amount from player funds

                for i in range(len(table.players)):
                    table.players[i].removeBlind(i)

                table.addCurrentBet(table.blindAmount*2)

                # shuffle and deal 1 card to each player
                deck.shuffleDeck()
                """
                ## can deal manually or with a for statement
                table.players[0].receiveCard(deck.dealCard())
                table.players[1].receiveCard(deck.dealCard())
                """
                for i in range(len(table.players)):
                    table.players[i].receiveCard(deck.dealCard())

                # each player bets
                table.handNotWon = betting()
                
                table.currentRound += 1
                
        elif (table.currentRound == 2) and handNotWon == True:
            print("Round 2: Table gets dealt one community card, then bet")
            # shuffle and deal 1 community card to the table
            deck.shuffleDeck()
            table.recieveCommunityCard(deck.dealCard())
            ####then betting
            handNotWon = betting()
            table.currentRound += 1
        elif (table.currentRound > 2) and handNotWon == True:
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
    print("\npress e to exit, or enter to continue:")
    exit = str(input("")).upper()
    if exit == "E":
        playingHand = False

print("End of game")