from DeckClass import Deck
from TableClass import Table

def NextPlayerOutput():
    ## tell players who the next player is and stop players from seeing each other's turns
    print("--------------------")
    print("Next player is:", table.players[0].getName())
    input("Understand and ready to start "+table.players[0].getName()+"'s turn? press enter to continue")
    for i in range(50):
        print("--------------------")     

############################################ main code ############################################
##global attributes
global table
table = Table()
playingHand = True

# begin game
while playingHand:
    print("Starting new hand")
    
    ## get array of players with funds
    table.getPlayersWithFunds()
    if (len(table.players) < 2):
        print("Not enough players with funds")
        playingHand = False
        break
    
    ## print player balances
    print("\n")
    for player in table.players:
        print(player.getName(),"has a balance of:", player.getBalance())
    
    ## create deck with 2 suits
    deck = Deck(2)

    ## start hand
    table.hand += 1
    print("\nHand",table.hand)
    while table.handNotWon:
        ## round 1
        if table.currentRound == 1:
            if table.players:
                print("Round 1: 1st player pays small blind (",table.blindAmount,"), second pays big blind (",table.blindAmount*2,"), get dealt a card, then bet")
                
                ## print next player
                NextPlayerOutput()
                
                # remove blinds from players and add to pot
                for i in range(len(table.players)):
                    table.players[i].removeBlind(i)
                table.addCurrentBet(table.blindAmount*2)

                 ## Deal cards manually (for testing)
                table.players[0].receiveCard(deck.dealSpecificCard("Queen"))
                table.players[1].receiveCard(deck.dealSpecificCard("Queen"))
                
                
                ## shuffle and deal 1 card to each player
                #deck.shuffleDeck()
                #for i in range(len(table.players)):
                #    table.players[i].receiveCard(deck.dealCard())

                # betting round
                table.handNotWon = table.betting()
                
                table.currentRound += 1
                
        ## round 2   
        elif (table.currentRound == 2) and table.handNotWon == True:
            print("\n----------------\nRound 2: Table gets dealt one community card, then bet")
            table.newRound()

            # shuffle and deal 1 community card to the table
            deck.shuffleDeck()
            table.recieveCommunityCard(deck.dealCard())
            
            ## print next player
            NextPlayerOutput()  

            # betting round
            table.betting()
            table.handNotWon = False
    
    ## Winner evaluation
    table.evaluateWinner()

    ## check if wants to play another hand
    print("\nWould you like to play another hand?")
    print("Press e to exit, or press enter to play new hand")
    exit = str(input("")).upper()
    if exit == "E":
        playingHand = False
    else:
        for i in range(50):
            print("--------------------")

print("Exiting application")

