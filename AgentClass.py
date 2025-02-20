from PlayerClass import Player
from Situations import SituationGenerator
import time
import random

class Agent(Player):
    def __init__(self,table, startingBalance, name):
        super().__init__(table, startingBalance, name)
        self.intentionClass = SituationGenerator()
        self.intentionClass.setFromFile()
        self.canCall = False
        self.canCheck = False
        self.canRaise = False
        #print("bot constructed")
        #self.threshhold = 0
        self.profile = {"tight/loose": 0.1, "agressive/passive": 0.9} # values between 0 and 1 on scale

    def chooseAction(self, canCheck, canCall, canRaise):
        self.getIntention(canCheck, canCall, canRaise)
        print("Waiting for agent decision", end="", flush = True)
        for i in range( random.randint(3, 9)):
            print(".", end="")
            time.sleep(1)
        return "check/call"

    def bet(self):
        print("")
        print (self.name, "'s turn to bet:")
        print ("Pot:", self.table.getPot())
        print ("Balance:", self.balance)
        print("Card:",self.currentCard.getName())
        action = ""
        diff = self.getDifference()
        
        self.canCall = False
        self.canCheck = False
        self.canRaise = False

        if (self.amountBetThisRound < self.table.getCurrentBet()): ## if bets not equal, needs to call to get to same amount
            if (self.balance >= diff): ##if has enough funds to call
                print(" - Call(",diff,")")
                self.canCall = True
        else:
            print(" - Check")
            self.canCheck = True
        
        if (self.timesRaisedThisRound < self.table.maxRaisesEach): ## if not past max bets, can raise
            if(self.balance >= diff + self.table.raiseAmount):
                print(" - Raise (",diff + self.table.raiseAmount,")")
                self.canRaise = True

        print(" - Fold")
        action = self.chooseAction(self.canCheck, self.canCall, self.canRaise)

        match action:
            case "call": # add to pot, matching check or raise
                self.removeFunds(diff)
            case "check/call":
                if self.canCall == True:
                    self.removeFunds(diff)
                    action = "call"
                else:
                    action = "check"
            case "raise": # raise by raise amount + any difference to previous player
                self.removeFunds(diff + self.table.raiseAmount)
                self.table.addCurrentBet(self.table.raiseAmount)
                self.timesRaisedThisRound += 1
            case "fold": # if everyone but one player folds, they automatically win the hand
                self.folded = True
                self.table.playerFolds(self)

        print("Agent performed",action,"action\n")

    def getIntention(self,canCheck, canCall, canRaise):
        canCallOrCheck = canCheck or canCall
        
        #moneyThreshold = 
        for i in self.intentionClass.intentions:
            print(i)

        print("should be:",self.table.currentRound,self.currentCard,canCallOrCheck,canRaise,"null",self.table.communityCard.getName())
        intentions = self.intentionClass.findIntentions(self.table.currentRound,self.currentCard.getName(),canCallOrCheck,canRaise,"null",self.table.communityCard.getName())

        # check closest profile score - agressiveness/looseness
        # check outcome against fund threshold - tight/loose
        # pick best based on closest profile, and outcome
        



