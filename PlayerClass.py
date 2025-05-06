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
        """
        ## this code is the unfinished code for custom profiles
        ## it gets an intention file (or creates one) using the player name
        ## it tries to get the action ratio stored at the start of the file
        
        self.intentions = table.getIntentionClass().setFromFile(name)
        if self.intentions[0].startswith("actionRatio"):
            print(self.intentions[0]) ## trying to get action ratio from start of intention file
            self.intentions.pop(0)
        """

    def resetHand(self):
        ## reset variables for new hand
        self.currentCard = Card(-1,"null")
        self.folded = False
        self.amountBetThisRound = 0
        self.timesRaisedThisRound = 0
    
    ## get functions
    def getBalance(self):
        return self.balance
    
    def getName(self):
        return self.name
    
    def getCurrentCard(self):
        return self.currentCard
    
    def getAmountBetThisRound(self):
        return self.amountBetThisRound
    
    ## other functions
    
    def addBalance(self, amount):
        self.balance += amount
    
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

    def removeBlind(self, position):
        ## if first, remove 1 (small blind) if not remove 2 (big blind)
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
        self.addAmountBetThisRound(amount)
        self.table.addToPot(amount)

    def addFunds(self, amount):
        self.balance += amount

    def chooseAction(self):
        ## perfroms user input validation to make sure the input is an acceptable action
        while True:
            try:
                action = str(input("")).lower()
            except:
                print("Please enter a string")
                continue
            if (action in self.actions):
                if ((action == "check")and(self.canCheck == False)):
                    print("You cannot check currently, enter valid action:")
                    continue
                elif((action == "call")and(self.canCall == False)):
                    print("You cannot call currently, enter valid action:")
                    continue
                elif((action == "raise")and(self.canRaise == False)):
                    print("You cannot raise as maximum raises per player is",self.table.addToPotmaxRaisesEach,", enter valid action:")
                    continue
                else:
                    break
            else:
                print(action)
                print("Please enter valid action")
        return action
    
    def info(self):
        ## output information for player
        print("")
        print (self.name, "'s turn to bet:")
        print ("Pot:", self.table.getPot())
        for player in self.table.players:
            if (player != self):
                print(player.getName()+"'s Funds:", player.getBalance())
        print ("Funds:", self.balance)
        print("Funds bet so far: ",self.amountBetThisRound)
        #print("Current bet to match:", self.table.getCurrentBet())
        if (self.table.getCommunityCard().getName() != "null"): 
            print ("\nCommunity Card:", self.table.getCommunityCard())
        print("Card:",self.currentCard.getName())  

    def bet(self):
        ## print information for player
        self.info()
        action = ""
        
        ## get difference between the amount bet this round by this player and the other player
        diff = self.getDifference()
        
        ## get and output available actions
        print("\nAvailable actions:")
        self.availableActions(diff)
        
        ## choose action
        action = self.chooseAction()
        
        self.GoToNextPlayer(action)

        ## perform the actions
        match action:
            case "call": # remove funds to match the bet
                self.removeFunds(diff)
            case "raise": # raise by raise amount + any difference to previous player
                self.removeFunds(diff + self.table.raiseAmount)
                self.table.addCurrentBet(self.table.raiseAmount)
                self.timesRaisedThisRound += 1
            case "fold": # if everyone but one player folds, they automatically win the hand
                self.folded = True
                self.table.playerFolds(self)
            ## CHECK = no adding to pot, matching previous bet, nothing is changed
        ## code for tracking actions for creating custom profiles
        ##self.recordIntentions(action)

    def availableActions(self, diff):
        self.canCall = False
        self.canCheck = False
        self.canRaise = False
        ## if bets are not equal, then can call (if has enough funds). If bets are equal, then can check
        if (self.amountBetThisRound < self.table.getCurrentBet()): 
            if (self.balance >= diff):
                print(" - Call(",diff,")")
                self.canCall = True
        else:
            print(" - Check")
            self.canCheck = True
        ## if not past max raises and has enough funds, then can raise
        if (self.timesRaisedThisRound < self.table.maxRaisesEach): 
            if(self.balance >= diff + self.table.raiseAmount):
                print(" - Raise (",diff + self.table.raiseAmount,")")
                self.canRaise = True
        ## can always fold
        print(" - Fold")

    def GoToNextPlayer(self, action):
        ## Output for playtesting
        for i in range(50):
            print("--------------------")
        print("Please hand over control to opponent")
        input("Ready for next player's turn? press enter to continue")
        for i in range(50):
            print("--------------------")

        print("Opponent performed",action,"action\n")

    """
    ## unused code for creating custom profiles of the player
    def recordIntentions(self, action):
        situation = []
        canCallOrCheck = self.canCall or self.canCheck
        communityCard = "null"
        if self.table.communityCard.getName() != "null":
            if self.table.communityCard == self.currentCard:
                communityCard = "same"
            else:
                communityCard = "diff"
             
        intentions = self.table.intentionClass.findIntentions(self.intentions, self.table.currentRound,self.currentCard.getName(),
                                                              canCallOrCheck,self.canRaise,"null",communityCard)
        print(intentions)
        currentIntention = []
        for intention in intentions:
            intentionAction = intention[-1]
            if (intention[-1] == "call/check"):
                if self.canCall == True:
                    intentionAction = "call"
                elif self.canCheck == True:
                    intentionAction = "check"
            if (intentionAction == action):
                currentIntention = intention
    """
