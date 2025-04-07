import random
from PlayerClass import Player
from AgentClass import Agent
from CardClass import Card

class Table:
    def __init__(self):
        
        self.possiblePlayers = [Player(self,10,"Eleanor"), Player(self,10,"AI/Ellie")]
        self.resetTable()
        self.blindAmount = 1
        self.maxRaisesEach = 2
        self.hand = 0
        self.raiseAmount = 2 * self.currentRound
        #print("table constructed") 

    def resetTable(self):
        self.players = []
        self.currentRound = 1
        self.handNotWon = True
        self.winner = -1
        self.firstPlayerIndex = random.randint(0, len(self.possiblePlayers) - 1)
        self.communityCard = Card(-1,"null")
        self.pot = 0
        self.currentBetAmount = 0
        self.continueBetting = True

    def getCommunityCard(self):
        return self.communityCard

    def recieveCommunityCard(self,card):
        self.communityCard = card
        print("Community card is a",self.communityCard.getName())

    def newRound(self):
         self.raiseAmount = 2 * self.current_round

    def addToPot(self, amount):
        self.pot += amount

    def getPot(self):
        return self.pot

    def addCurrentBet(self, amount):
        self.currentBetAmount += amount
        
    def getCurrentBet(self):
        return self.currentBetAmount

    def playerFolds(self, player):
        self.players.remove(player)
        #self.playersFolded += 1
        #if (len(players) - self.playersFolded <= 1):
        if (len(self.players) < 2):
            print("all but one player folded")
            self.continueBetting = False

    def getCurrentPlayers(self):
        return self.players
    
    def playersHaveFunds(self, player):
        if (player.availableFunds(self.blindAmount) == True):
            self.players.append(player)
        else:
            print(player.getName()," does not have enough funds for the blind")

    def getPlayersWithFunds(self):
        self.players = []

        ## puts players that have enough funds in a list, in order, starting with the first player
        for i in range(len(self.possiblePlayers)):
            if (i + self.firstPlayerIndex) < len(self.possiblePlayers):
                self.playersHaveFunds(self.possiblePlayers[i + self.firstPlayerIndex])
            else:
                self.playersHaveFunds(self.possiblePlayers[(i + self.firstPlayerIndex) - len(self.possiblePlayers)])
        
        """
        ## shows order of players
        for player in self.players:
            print(player.getName())
        """

    def betting(self): ##returns is hand is won yet or not
        stillBetting = True
        i = 0
        while stillBetting:
            if (self.currentDifferenceInBets() != 0) or i == 0:
                for player in self.players:
                    if (player.folded == False) and (self.continueBetting == True):
                        player.bet()
                    if (self.continueBetting == False):
                        stillBetting == False
                        return False
            if (self.currentDifferenceInBets() == 0):
                stillBetting = False
            i += 1
        return True

    def currentDifferenceInBets(self):
        diff = 0
        for player in self.players:
            diff += player.getDifference()
        return diff

    def evaluateWinner(self):
        winnerIndexes = []
        if len(self.players) == 1:
            #print("all but one player folded")
            winnerIndexes = [0]
        else:
            for i in range(len(self.players)):
                if self.players[i].getCurrentCard().getValue() == self.getCommunityCard().getValue():
                    winnerIndexes = [i]
                    
            if winnerIndexes == []: ## if the card is no the same for any of the players
                playerCardValues = []
                for i in range(len(self.players)):
                    
                    card = self.players[i].getCurrentCard().getValue()
                    print(self.players[i].getName(), card)
                    playerCardValues.append(card)

                maxValue = -1
                for i in range(len(playerCardValues)):
                    if playerCardValues[i] > maxValue:
                        winnerIndexes = [i]
                        maxValue = playerCardValues[i]
                    elif playerCardValues[i] == maxValue:
                        winnerIndexes.append(i)
                print(maxValue)
        self.awardWinnings(winnerIndexes)
    
    def awardWinnings(self, winnerIndexes):
        len(winnerIndexes) 
        if len(winnerIndexes) == 1:
            winner = self.players[winnerIndexes[0]]
            print("\nThe winner is",winner.getName(), "with a", winner.getCurrentCard().getName())
            winner.addFunds(self.getPot())
        else:
            print("\nThere is multiple winners, the pot is split between ", end="", flush = True)
            for i in range(len(winnerIndexes)):
                print(self.players[winnerIndexes[i]].getName(), end="", flush = True)
                if i != len(winnerIndexes)-1:
                    print(" and ", end="", flush = True)
                self.players[winnerIndexes[i]].addFunds(self.getPot()//len(winnerIndexes))
            print("")
        for player in self.possiblePlayers:
            player.resetHand()
        self.resetTable()




