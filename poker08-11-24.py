import random
##objects
class Card:
    def __init__(self,value):
        self.value = value
        #print("card constructed")

    def __str__(self):
        return f"{self.value}"

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
    
class Table:
    def __init__(self):
       self.communityCard = Card(-1)
       self.pot = 0
       print("table constructed") 

    def getCommunityCard(self):
        return self.communityCard

    def recieveCommunityCard(self,card):
        self.communityCard = card

    def addToPot(self, amount):
        self.pot += amount

    def getPot(self):
        return self.pot

class Player:
    def __init__(self,startingBalance, name):
        self.balance = startingBalance
        self.amountBetThisRound = 0
        self.timesRaisedThisRound = 0
        self.currentCard = Card(-1)
        self.name = name
        self.actions = ["CHECK","CALL","RAISE","FOLD"]

        #print("player constructed")

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
        
    def changeAmountBetThisRound(self, amount):
        self.amountBetThisRound += amount
    
    def resetAmountBetThisRound(self):
        self.amountBetThisRound = 0

    def getAmountBetThisRound(self):
        return self.amountBetThisRound

    def changeFunds(self, amount):
        #print(self.name, " Balance: ", self.balance)
        self.balance += amount
        #print("Amount: ", amount)
        print(self.name, "New balance: ", self.balance)
        if(amount < 0):
            self.changeAmountBetThisRound(-amount)

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
                    print("You cannot raise as maximum raises each is",maxRaisesEach,", enter valid action:")
                    continue
                else:
                    break
            else:
                print("Please enter valid action")
        return action

        

    def bet(self, previousPlayer):
        action = ""

        print("amount bet so far: ",self.amountBetThisRound)
        print("previous player amount: ",previousPlayer.getAmountBetThisRound())

        diff = previousPlayer.getAmountBetThisRound() - self.getAmountBetThisRound()
        if diff < 0:
            diff = 0
        print(diff)

        print("Enter action from available actions:")
        canCall = False
        canCheck = False
        canRaise = False
        if (self.amountBetThisRound < previousPlayer.getAmountBetThisRound()): ## if bets not equal, needs to call to get to same amount
            if (self.balance >= diff):
                print("Call")
                canCall = True
        else:
            print("Check")
            canCheck = True
        
        if (self.timesRaisedThisRound < maxRaisesEach): ## if not past max bets, can raise
            if(self.balance >= diff+raiseAmount):
                print("Raise")
                canRaise = True

        print("Fold")
        action = self.getValidAction(canCheck, canCall, canRaise)

        match action:
            case "CALL":
                print("call = add to pot, matching previous bet")
            case "CHECK":
                print("check = no adding to pot, matching previous bet - just using blinds")
            case "RAISE":
                print("raise = raise by 2 chips")
                self.timesRaisedThisRound =+ 1
            case "FOLD":
                print("fold = lose")
            case _:
                print("ERROR")
            


##global attributes
p1 = Player(7,"1")
p2 = Player(4, "2")
#p3 = Player(2, "3")
#possiblePlayers = [p1,p2,p3]
possiblePlayers = [p1,p2]
blindAmount = 2
maxRaisesEach = 2
raiseAmount = 2
pot = 0
turn = 0
deck = Deck()

## global functions
def getPreviousPlayerIndex(index):
    previousPlayer = index - 1
    if (previousPlayer < 0):
        previousPlayer = len(players) -1
    return previousPlayer

############################################ main code ############################################
playersWithFunds = True
hand = 0
# begin game
while playersWithFunds:
    ## get list of players with funds
    players = []
    for player in possiblePlayers:
        if (player.availableFunds(blindAmount) == True):
            players.append(player)
        else:
            print(player.getName()," does not have enough funds for the blind")
    if (len(players) < 2):
        print("Not enough players with funds")
        playersWithFunds = False
        break
    
    hand += 1
    print("Hand",hand)
    roundOfPlay = 1
    handNotWon = True
    ## begin hand
    while handNotWon:
        if roundOfPlay == 0:
            #print(players[0].getName() + "'s starting bankroll: ",players[0].getBalance())
            #print(players[1].getName() + "'s starting bankroll: ",players[1].getBalance())
            roundOfPlay += 1
        elif roundOfPlay == 1:
            if players:
                # remove blind amount from player funds
                for player in players: 
                    player.changeFunds(- blindAmount) 
                # shuffle and deal 1 card to each player
                players[1].changeFunds(-blindAmount) 
                deck.shuffleDeck()
                for i in range(len(players)):
                    players[i].receiveCard(deck.dealCard())
                # each player bets
                for i in range(len(players)):
                    print ("Player ", players[i].getName(), " turn to bet:")
                    previousPlayer = getPreviousPlayerIndex(i)
                    players[i].bet(players[previousPlayer])
                ##### should not be able to raise more than 2 times each
                ##### check still 2 player not folded
                roundOfPlay += 1
        elif roundOfPlay == 2:
            roundOfPlay += 1

            # shuffle and deal 1 community card to the table
            deck.shuffleDeck()
            #Table.recieveCommunityCard(deck.dealCard())
            ####then betting
        else:
            print("Evaluation")
            ####same value as public card wins
            ####if neither same, highest wins
            handNotWon = False
            print("End of hand")

print("End of game")