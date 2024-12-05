import random

##objects
class Card:
    def __init__(self,value):
        self.value = value
        #print("card constructed")

    def __str__(self):
        return f"{self.value}"

###################################################################
class Deck:
    def __init__(self):
        self.values = ["Jack","Queen","King"]
        self.cards = self.makeDeck(2,self.values)
        #print("deck constructed")

    def makeDeck(self, suits, values):
        cards = []
        for suit in range(suits):
            for value in range(len(values)):
                cards.append(Card(values[value-1]))
        return cards

    def printDeck(self):
        print("Cards:")
        for i in self.cards:
            print(i)

    def shuffleDeck(self):
        tempCards = [len(self.cards)]
        while (len(self.cards) > 0):
            randNum = random.randrange(0, len(self.cards))
            tempCards.append(self.cards[randNum])
            self.cards.pop(randNum)
        self.cards = tempCards

    def dealCard(self):
        return self.cards.pop()

###################################################################
class Table:
    def __init__(self):
        self.players = []
        self.resetTable()
        self.blindAmount = 10
        self.maxRaisesEach = 2
        self.raiseAmount = 20
        p1 = Player(700,"1")
        p2 = Player(400, "2")
        self.possiblePlayers = [p1,p2]
        #print("table constructed") 

    def resetTable(self):
        self.communityCard = Card(-1)
        self.pot = 0
        self.currentBetAmount = 0
        self.continueBetting = True

    def getCommunityCard(self):
        return self.communityCard

    def recieveCommunityCard(self,card):
        self.communityCard = card

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

    def endOfHand(self):
        for player in self.players:
            player.resetHand()
        self.resetTable()
        
###################################################################
class Player:
    def __init__(self,startingBalance, name):
        self.balance = startingBalance
        self.resetHand()
        self.name = name
        self.actions = ["CHECK","CALL","RAISE","FOLD"]
        #print("player constructed")

    def resetHand(self):
        self.currentCard = Card(-1)
        self.folded = False
        self.amountBetThisRound = 0
        self.timesRaisedThisRound = 0

    def getBalance(self):
        return self.balance
    
    def getName(self):
        return self.name
    
    def getCurrentCard(self):
        return self.currentCard
    
    def receiveCard(self,card):
        self.currentCard = card

    def availableFunds(self,amount):
        if (amount > self.balance):
            print("Not enough funds in ",self.name,"'s bankroll")
            return False
        else:
            return True
        
    def getDifference(self):
        diff = table.getCurrentBet() - self.getAmountBetThisRound()
        diff = max(diff,0)
        ##print("difference:",diff)
        return diff
        
    def addAmountBetThisRound(self, amount):
        self.amountBetThisRound += amount
    
    def resetAmountBetThisRound(self):
        self.amountBetThisRound = 0

    def getAmountBetThisRound(self):
        return self.amountBetThisRound

    def removeBlind(self):
        self.balance -= table.blindAmount
        self.addAmountBetThisRound(table.blindAmount)

    def removeFunds(self, amount):
        self.balance -= amount
        print(self.name, "New balance: ", self.balance)
        self.addAmountBetThisRound(amount)
        table.addCurrentBet(amount)

    def addFunds(self, amount):
        self.balance += amount
        print(self.name, "New balance: ", self.balance)

    def getValidAction(self, canCheck, canCall, canRaise):
        while True:
            try:
                action = str(input("")).upper()
            except:
                print("Please enter a string")
                continue
            if (action in self.actions):
                if ((action == "CHECK")and(canCheck == False)):
                    print("You cannot check currently, enter valid action:")
                    continue
                elif((action == "CALL")and(canCall == False)):
                    print("You cannot call currently, enter valid action:")
                    continue
                elif((action == "RAISE")and(canRaise == False)):
                    print("You cannot raise as maximum raises per player is",table.addToPotmaxRaisesEach,", enter valid action:")
                    continue
                else:
                    break
            else:
                print("Please enter valid action")
        return action

    def bet(self):
        print("Card:",self.currentCard)
        action = ""

        print("amount bet so far: ",self.amountBetThisRound)
        print("current betting balance:", table.getCurrentBet())

        diff = self.getDifference()

        print("\nEnter action from available actions:")
        canCall = False
        canCheck = False
        canRaise = False
        if (self.amountBetThisRound < table.getCurrentBet()): ## if bets not equal, needs to call to get to same amount
            if (self.balance >= diff): ##if has enough funds to call
                print("Call")
                canCall = True
        else:
            print("Check")
            canCheck = True
        
        if (self.timesRaisedThisRound < table.maxRaisesEach): ## if not past max bets, can raise
            if(self.balance >= diff + table.raiseAmount):
                print("Raise")
                canRaise = True

        print("Fold")
        action = self.getValidAction(canCheck, canCall, canRaise)
        print("\n")

        match action:
            case "CALL":
                self.removeFunds(diff)
                #print("call = add to pot, matching check or raise")
            case "CHECK":
                print("check = no adding to pot, matching previous bet - e.g. just using blinds")
            case "RAISE":
                print("raise = raise by raise amount")
                self.removeFunds(table.raiseAmount)
                self.timesRaisedThisRound =+ 1
            case "FOLD":
                self.folded = True
                table.playerFolds(self)
                print("fold = lose")
            case _:
                print("ERROR")
##################################################################################################

## global functions
"""def getPreviousPlayerIndex(index):
    previousPlayer = index - 1
    if (previousPlayer < 0):
        previousPlayer = len(players) -1
    return previousPlayer"""

def betting():
    """
    for i in range(len(table.players)):
        print ("\nPlayer ", table.players[i].getName(), " turn to bet:")
        if (table.players[i].folded == False) and (table.continueBetting == True):
            table.players[i].bet()
        if (table.continueBetting == False):
            winner = table.players
            handNotWon = False"""
    stillBetting = True
    i = 0
    while stillBetting:
        if (table.currentDifferenceInBets() != 0) or i == 0:
            for player in table.players:
                print ("\nPlayer ", player.getName(), " turn to bet:")
                if (player.folded == False) and (table.continueBetting == True):
                    player.bet()
                if (table.continueBetting == False):
                    #winner = 0
                    handNotWon = False
                    print("here")
                    stillBetting == False
                    break
        if (table.currentDifferenceInBets() == 0):
            stillBetting == False
        i += 1
    print("there")

    

def evaluateWinner():
    return -1

############################################ main code ############################################
##global attributes
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
                print("Round 1")
                print("    Give blinds, get dealt a card, then bet")
                # remove blind amount from player funds
                for player in table.players: 
                    player.removeBlind()
                table.addCurrentBet(table.blindAmount)

                # shuffle and deal 1 card to each player
                deck.shuffleDeck()
                for i in range(len(table.players)):
                    table.players[i].receiveCard(deck.dealCard())

                # each player bets
                betting()
                
                roundOfPlay += 1
        elif (roundOfPlay == 2) and handNotWon == True:
            print("Round 2")
            print("    get dealt one community card to table, then bet")
            # shuffle and deal 1 community card to the table
            deck.shuffleDeck()
            table.recieveCommunityCard(deck.dealCard())
            ####then betting
            betting()
            roundOfPlay += 1
        elif (roundOfPlay > 2) and handNotWon == True:
            print("Evaluation")
            ####same value as public card wins
            ####if neither same, highest wins
            handNotWon = False
            
    print("End of hand")
    ####award money here
    table.players[winner].addFunds(table.getPot())
    table.endOfHand()

    ## check still playing
    print("\npress e to exit:")
    exit = str(input("")).upper()
    if exit == "E":
        playing = False

print("End of game")