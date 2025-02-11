import random
from PlayerClass import Player
from AgentClass import Agent
from CardClass import Card

class Table:
    def __init__(self):
        self.players = []
        self.possiblePlayers = [Player(self,10,"Human"), Agent(self,10,"Agent"), Agent(self,0,"Floof")]
        #self.firstPlayer = 0
        
        self.resetTable()
        
        self.blindAmount = 1
        self.maxRaisesEach = 2
        self.hand = 0
        self.raiseAmount = 2 * self.currentRound
        #print("table constructed") 

    def resetTable(self):
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
        print(card)
        self.communityCard = card
        print("Community card is a",self.communityCard.getValue())
        print("Community card is a",self.communityCard.getName())

    def newRound(self):
         self.raiseAmount =2 * self.current_round

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
            print("all or all but one player folded")
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

    def currentDifferenceInBets(self):
        diff = 0
        for player in self.players:
            diff += player.getDifference()
        return diff

    def endOfHand(self, winnerIndexes):
        len(winnerIndexes) 
        if len(winnerIndexes) == 1:
            self.players[winnerIndexes[0]].addFunds(self.getPot())
        else:
            for playerIndex in winnerIndexes:
                self.players[playerIndex].addFunds(self.getPot()//len(winnerIndexes))
        for player in self.players:
            player.resetHand()
        self.resetTable()




