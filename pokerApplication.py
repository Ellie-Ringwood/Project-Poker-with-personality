import random
from CardClass import Card
from DeckClass import Deck
from TableClass import Table
from PlayerClass import Player

############################################ main code ############################################
##global attributes
global table
table = Table()
playingHand = True

# begin game
while playingHand:

    ## get list of players with funds
    print("starting new hand")
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
    
    
    deck = Deck(2)

    while table.handNotWon:
        if table.currentRound == 1:
            if table.players:
                print("Round 1: 1st player pays small blind (",table.blindAmount,"), second pays big blind (",table.blindAmount*2,"), get dealt a card, then bet")
                # remove blind amount from player funds

                #print("lenght of players:", len(table.players))

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
                table.handNotWon = table.betting()
                
                table.currentRound += 1
                
        elif (table.currentRound == 2) and table.handNotWon == True:
            print("\n----------------\nRound 2: Table gets dealt one community card, then bet")
            # shuffle and deal 1 community card to the table
            deck.shuffleDeck()
            table.recieveCommunityCard(deck.dealCard())
            ####then betting
            table.handNotWon = table.betting()
            table.currentRound += 1
        elif (table.currentRound > 2) and table.handNotWon == True:
            print("\nEvaluation")
            
            table.handNotWon = False
    
    ####same value as public card wins
    ####if neither same, highest wins
    ####award money here
    table.evaluateWinner()
    print("End of hand")

    ## check still playing
    print("\npress e to exit, or enter to continue:")
    exit = str(input("")).upper()
    if exit == "E":
        playingHand = False

print("End of game")