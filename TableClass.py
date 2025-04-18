import random
from PlayerClass import Player
from AgentClass import Agent
from CardClass import Card
from Situations import SituationGenerator

class Table:
    def __init__(self):
        ## create communial intention class, so its niot repeated by each agent
        self.intentionClass = SituationGenerator()
        ## enter players, starting funds and names
        self.possiblePlayers = [Player(self,20,"M"), Agent(self,20,"AI/Ellie","TA")]
        ## set variables for the game
        self.resetTable()
        self.blindAmount = 1
        self.maxRaisesEach = 2
        self.hand = 0
        #print("table constructed") 

    def resetTable(self):
        ## reset variables to be correct for start of new hand
        self.players = []
        self.currentRound = 1
        self.handNotWon = True
        self.firstPlayerIndex = random.randint(0, len(self.possiblePlayers) - 1)
        self.communityCard = Card(-1,"null")
        self.pot = 0
        self.currentBetAmount = 0
        self.continueBetting = True
        self.raiseAmount = 2 * self.currentRound
   
    ## get functions
    def getCommunityCard(self):
        return self.communityCard

    def getCurrentBet(self):
        return self.currentBetAmount
    
    def getPot(self):
        return self.pot
    
    def getIntentionClass(self):
        return self.intentionClass

    ## other functions
    def recieveCommunityCard(self,card):
        self.communityCard = card
        print("Community card is a",self.communityCard.getName())

    def newRound(self):
        ## changes raise amount for second round
        self.raiseAmount = 2 * self.current_round

    def addToPot(self, amount):
        self.pot += amount

    def addCurrentBet(self, amount):
        self.currentBetAmount += amount

    def playerFolds(self, player):
        ## when a player folds they are removed from the current hand
        self.players.remove(player)
        if (len(self.players) < 2):
            print("All but one player folded")
            self.continueBetting = False
     
    def playersHaveFunds(self, player):
        ## appends players that have funds to the player array
        if (player.availableFunds(self.blindAmount*2) == True):
            self.players.append(player)
        else:
            print(player.getName()," does not have enough funds for the blind")

    def getPlayersWithFunds(self):
        self.players = []
        ## puts players that have enough funds in a list, in order, starting with the first player
        for i in range(len(self.possiblePlayers)):
            if (i + self.firstPlayerIndex) < len(self.possiblePlayers):
                ## if next index is not more than the array, set it normally
                self.playersHaveFunds(self.possiblePlayers[i + self.firstPlayerIndex])
            else:
                ## if next index is more than the array, set it to loop back to beginning
                self.playersHaveFunds(self.possiblePlayers[(i + self.firstPlayerIndex) - len(self.possiblePlayers)])

    
    def betting(self): ## returns if hand is not won yet (true) or it is won (false)
        stillBetting = True
        i = 0
        while stillBetting:
            if (self.calcCurrentDifferenceInBets() != 0) or i == 0:
                ## if player bets are not equal or is first bet (i == 0), repeat
                for player in self.players:
                    ## each player bets
                    if (player.folded == False) and (self.continueBetting == True):
                        player.bet()
                    if (self.continueBetting == False):
                        ## player has folded, so a player has won, so returns false
                        stillBetting == False
                        return False
            if (self.calcCurrentDifferenceInBets() == 0):
                ## if player bets are equal, stop repeating
                stillBetting = False
            i += 1
        ## if reaches here, the hand is not won
        return True

    def calcCurrentDifferenceInBets(self):
        # calculates the difference between player's bets
        diff = 0
        for player in self.players:
            diff += player.getDifference()
        return diff

    def evaluateWinner(self):
        ## winner indexes allows for multiple winners (a draw)
        winnerIndexes = []
        if len(self.players) == 1:
            ## if all players have folded but one, then that player has won
            winnerIndexes = [0]
        else:
            ## evaluate cards if more than one unfolded player
            for i in range(len(self.players)):
                if self.players[i].getCurrentCard().getValue() == self.getCommunityCard().getValue():
                    ## if player has same card as community card they win automatically
                    winnerIndexes = [i]
             
            if winnerIndexes == []: 
                ## if no player has the same card as the community card, evaluate highest card value
                playerCardValues = []
                for i in range(len(self.players)):
                    ## get each player's card values
                    card = self.players[i].getCurrentCard().getValue()
                    playerCardValues.append(card)

                ## get highest value card and it's player's index
                maxValue = -1
                for i in range(len(playerCardValues)):
                    if playerCardValues[i] > maxValue:
                        ## if higher value than max value, is the new max value
                        winnerIndexes = [i]
                        maxValue = playerCardValues[i]
                    elif playerCardValues[i] == maxValue:
                        ## if same, then draw
                        winnerIndexes.append(i)
        ## award money
        self.awardWinnings(winnerIndexes)
    
    def awardWinnings(self, winnerIndexes):
        if len(winnerIndexes) == 1:
            ## if only one winner award pot to player
            winner = self.players[winnerIndexes[0]]
            print("\nThe winner is",winner.getName(), "with a", winner.getCurrentCard().getName())
            winner.addFunds(self.getPot())
        else:
            ## if multiple winners there is a draw
            ## print out names of winners nicely
            print("\nThere are multiple winners, each with a",self.players[winnerIndexes[0]].getCurrentCard().getName())
            print("The pot is split between ", end="", flush = True)
            for i in range(len(winnerIndexes)):
                print(self.players[winnerIndexes[i]].getName(), end="", flush = True)
                if i != len(winnerIndexes)-1:
                    print(" and ", end="", flush = True)
                ## award pot equally among the drawing players
                self.players[winnerIndexes[i]].addFunds(self.getPot()//len(winnerIndexes))
            print("")
        ## end this hand
        for player in self.possiblePlayers:
            player.resetHand()
        self.resetTable()




