import random

##objects
class Card:
    def __init__(self,value, name):
        self.value = value
        self.name = name
        #print("card constructed")

    def getValue(self):
        return self.value
    
    def getName(self):
        return self.name

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
                #cards.append(Card(values[value-1]))
                cards.append(Card(value,values[value-1]))
                print(value,values[value-1])
        return cards

    def printDeck(self):
        print("Cards:")
        for i in self.cards:
            print(i)

    def shuffleDeck(self):
        tempCards = []
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
        if len(winnerIndexes) == 1:
            table.players[winnerIndexes[0]].addFunds(table.getPot())
        else:
            print("multiple winners")
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
        self.currentCard = Card(-1,"null")
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
        table.addToPot(table.blindAmount)

    def removeFunds(self, amount):
        self.balance -= amount
        #print(self.name, "New balance: ", self.balance)
        self.addAmountBetThisRound(amount)
        table.addToPot(amount)

    def addFunds(self, amount):
        self.balance += amount
        #print(self.name, "New balance: ", self.balance)

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
        print ("\nPlayer ", self.name, " turn to bet:")
        print ("Pot:", table.getPot())
        print ("Balance:", self.balance)
        print("Card:",self.currentCard.getName())
        action = ""

        print("Funds bet so far: ",self.amountBetThisRound)
        print("Current bet to match:", table.getCurrentBet())

        diff = self.getDifference()

        print("\nEnter action from available actions:")
        canCall = False
        canCheck = False
        canRaise = False
        if (self.amountBetThisRound < table.getCurrentBet()): ## if bets not equal, needs to call to get to same amount
            if (self.balance >= diff): ##if has enough funds to call
                print("Call(",diff,")")
                canCall = True
        else:
            print("Check")
            canCheck = True
        
        if (self.timesRaisedThisRound < table.maxRaisesEach): ## if not past max bets, can raise
            if(self.balance >= diff + table.raiseAmount):
                print("Raise (",diff + table.raiseAmount,")")
                canRaise = True

        print("Fold")
        action = self.getValidAction(canCheck, canCall, canRaise)

        match action:
            case "CALL": # add to pot, matching check or raise
                self.removeFunds(diff)
            case "RAISE": # raise by raise amount + any difference to previous player
                self.removeFunds(diff + table.raiseAmount)
                table.addCurrentBet(table.raiseAmount)
                self.timesRaisedThisRound += 1
            case "FOLD": # if everyone but one player folds, they automatically win the hand
                self.folded = True
                table.playerFolds(self)
        ## CHECK = no adding to pot, matching previous bet - e.g. just using blinds
                
##################################################################################################

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
    print("eval")

    for i in range(len(table.players)):
        if table.players.getCurrentCard().getValue() == table.getCommunityCard().getValue():
            winnerIndexes = [i]

    winnerIndexes = []
    playerValues = []
    for i in range(len(table.players)):
        card = table.players[i].getCurrentCard().getValue()
        playerValues.append(card)
    print(playerValues)

    ###### Do highest value hand evaluation, allow for multiple winners
            

        
    return winnerIndexes

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

    for player in table.players:
        print("Player",player.getName(),"has a balance of:", player.getBalance())

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
                for i in range(len(table.players)):
                    table.players[i].receiveCard(deck.dealCard())

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
        print("1 unfolded player left")
        table.endOfHand([0])
    else:
        print("multiple unfolded players left")
        table.endOfHand(evaluateWinner())

    ## check still playing
    print("\npress e to exit:")
    exit = str(input("")).upper()
    if exit == "E":
        playing = False

print("End of game")