from player import Player
from agent import Agent
from card import Card

class Table:
    def __init__(self):
        self.players = []
        self.resetTable()
        self.blindAmount = 1
        self.maxRaisesEach = 2
        self.current_round = 1
        self.raiseAmount = 2*self.current_round
        p1 = Player(7,"Human")
        agent = Agent(4,"Agent")
        #p2 = Player(400, "2")
        self.possiblePlayers = [p1,agent]
        #print("table constructed") 

    def resetTable(self):
        self.communityCard = Card.Card(-1,"null")
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

    def getPlayersWithFunds(self):
        self.players = []
        for player in self.possiblePlayers:
            if (player.availableFunds(self.blindAmount) == True):
                self.players.append(player)
            else:
                print(player.getName()," does not have enough funds for the blind")

    def currentDifferenceInBets(self):
        diff = 0
        for player in self.players:
            diff += player.getDifference()
        return diff

    def endOfHand(self, winnerIndexes):
        len(winnerIndexes) 
        if len(winnerIndexes) == 1:
            table.players[winnerIndexes[0]].addFunds(table.getPot())
        else:
            for playerIndex in winnerIndexes:
                table.players[playerIndex].addFunds(table.getPot()//len(winnerIndexes))
        for player in self.players:
            player.resetHand()
        self.resetTable()




