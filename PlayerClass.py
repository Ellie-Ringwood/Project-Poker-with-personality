#from table import Table
from CardClass import Card

class Player():
    def __init__(self, table, startingBalance, name):
        self.table = table
        self.balance = startingBalance
        self.resetHand()
        self.name = name
        self.actions = ["check","call","raise","fold"]
        self.canCall = False
        self.canCheck = False
        self.canRaise = False
        #print("player constructed")

    def resetHand(self):
        self.currentCard = Card(-1,"null")
        self.folded = False
        self.amountBetThisRound = 0
        self.timesRaisedThisRound = 0

    def getBalance(self):
        return self.balance
    
    def addBalance(self, amount):
        self.balance += amount
    
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
        diff = self.table.getCurrentBet() - self.getAmountBetThisRound()
        diff = max(diff,0)
        ##print("difference:",diff)
        return diff
        
    def addAmountBetThisRound(self, amount):
        self.amountBetThisRound += amount
    
    def resetAmountBetThisRound(self):
        self.amountBetThisRound = 0

    def getAmountBetThisRound(self):
        return self.amountBetThisRound

    def removeBlind(self, position):
        blind = 0
        if(position == 0):
            blind = self.table.blindAmount
        else:
            blind = self.table.blindAmount*2
        
        self.addBalance(-blind)
        self.addAmountBetThisRound(blind)
        self.table.addToPot(blind)

    def removeFunds(self, amount):
        self.balance -= amount
        #print(self.name, "New balance: ", self.balance)
        self.addAmountBetThisRound(amount)
        self.table.addToPot(amount)

    def addFunds(self, amount):
        self.balance += amount
        #print(self.name, "New balance: ", self.balance)

    def getValidAction(self, canCheck, canCall, canRaise):
        while True:
            try:
                action = str(input("")).lower()
            except:
                print("Please enter a string")
                continue
            if (action in self.actions):
                if ((action == "check")and(canCheck == False)):
                    print("You cannot check currently, enter valid action:")
                    continue
                elif((action == "call")and(canCall == False)):
                    print("You cannot call currently, enter valid action:")
                    continue
                elif((action == "raise")and(canRaise == False)):
                    print("You cannot raise as maximum raises per player is",self.table.addToPotmaxRaisesEach,", enter valid action:")
                    continue
                else:
                    break
            else:
                print(action)
                print("Please enter valid action")
        return action

    def bet(self):
        print("")
        print (self.name, "'s turn to bet:")
        print ("Pot:", self.table.getPot())
        print ("Balance:", self.balance)
        print("Card:",self.currentCard.getName())
        action = ""

        print("Funds bet so far: ",self.amountBetThisRound)
        print("Current bet to match:", self.table.getCurrentBet())

        diff = self.getDifference()

        print("\nEnter action from available actions:")
        self.canCall = False
        self.canCheck = False
        self.canRaise = False
        if (self.amountBetThisRound < self.table.getCurrentBet()): ## if bets not equal, needs to call to get to same amount
            if (self.balance >= diff): ##if has enough funds to call
                print(" - Call (",diff,")")
                self.canCall = True
        else:
            print(" - Check")
            self.canCheck = True
        
        if (self.timesRaisedThisRound < self.table.maxRaisesEach): ## if not past max bets, can raise
            if(self.balance >= diff + self.table.raiseAmount):
                print(" - Raise (",diff + self.table.raiseAmount,")")
                self.canRaise = True

        print(" - Fold")
        action = self.getValidAction(self.canCheck,self.canCall, self.canRaise)

        match action:
            case "call": # add to pot, matching check or raise
                self.removeFunds(diff)
            case "raise": # raise by raise amount + any difference to previous player
                self.removeFunds(diff + self.table.raiseAmount)
                self.table.addCurrentBet(self.table.raiseAmount)
                self.timesRaisedThisRound += 1
            case "fold": # if everyone but one player folds, they automatically win the hand
                self.folded = True
                self.table.playerFolds(self)
        ## CHECK = no adding to pot, matching previous bet - e.g. just using blinds



