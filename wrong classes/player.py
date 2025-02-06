#from table import Table
from card import Card

class Player():
    def __init__(self,startingBalance, name):
        global table
        self.balance = startingBalance
        self.resetHand()
        self.name = name
        self.actions = ["CHECK","CALL","RAISE","FOLD"]
        #print("player constructed")

    def resetHand(self):
        self.currentCard = Card.Card(-1,"null")
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
        print("")
        print (self.name, "'s turn to bet:")
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
                print(" - Call(",diff,")")
                canCall = True
        else:
            print(" - Check")
            canCheck = True
        
        if (self.timesRaisedThisRound < table.maxRaisesEach): ## if not past max bets, can raise
            if(self.balance >= diff + table.raiseAmount):
                print(" - Raise (",diff + table.raiseAmount,")")
                canRaise = True

        print(" - Fold")
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





