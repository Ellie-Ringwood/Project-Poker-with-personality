from PlayerClass import Player
from Situations import SituationGenerator
from CardClass import Card
import time
import random

class Agent(Player):
    def __init__(self,table, startingBalance, name):
        super().__init__(table, startingBalance, name)
        self.intentionClass = SituationGenerator()
        self.intentionClass.setFromFile()
        #self.resetHand()
        self.canCall = False
        self.canCheck = False
        self.canRaise = False

        self.profiles = self.intentionClass.scoreOrder
        self.targetActionRatios = [[0.9, 0.6, 0.4, 0.5],[0.6, 0.5, 0.1, 0.7],[0.6, 0.8, 0.7, 0.2],[0.6, 0.9, 0.6, 0.4]] #check-call-raise-fold ratios for each profile
        
        self.profile = "TA"
        self.targetActionRatio = []
        for i in range(len(self.profiles)):
            if self.profile == self.profiles[i]:
                self.targetActionRatio = self.targetActionRatios[i]
        
        self.emptyActionDict = {"check":0,"call":0, "raise":0, "fold":0}
        self.currentActionRatio = self.emptyActionDict
        self.actionCount = self.emptyActionDict
        self.totalActionCount = 0
        print(self.targetActionRatio)
        #print("bot constructed")

    def chooseAction(self, canCheck, canCall, canRaise):
        intentions = self.getIntentions(canCheck, canCall, canRaise)
        
        # get score for this profile from each action    
        intentionPreference = []  
        for intention in intentions:
            action = intention[2]
            scores = intention[1]
            score = 0
            for i in range(len(self.profiles)):
                if(self.profiles[i] ==self. profile):
                    score = scores[i]
            intentionPreference.append([action,score])
        #print(intentionPreference)

        # get preference to action based on action ratios
        
        for intention in intentions:
            tempActionRatio = self.increaseActionCount(intention)

        """
        #pick random intention
        rand = random.randint(0,len(intentions)-1)
        chosenIntention = intentions[rand]
        #print(chosenIntention)
        action = chosenIntention[2]
        """

        print("Waiting for agent decision", end="", flush = True)
        for i in range(random.randint(4,10)):
            print(".", end="")
            time.sleep(0.5)

        return action
    
    def increaseActionCount(self, intention):
        tempActionCount = self.actionCount    ######ISSUES WITH SELF.ACTION COUNT
        tempTotalActionCount = self.totalActionCount
            
        print(self.actionCount,tempTotalActionCount)
            
        action = str(intention[2])
        action = action.strip("'")
            
        if (action == "call/check"):
            if self.canCall == True:
                action = "call"
            elif self.canCheck == True:
                action = "check"
                    
        tempActionCount[action] += 1;
        tempTotalActionCount += 1

        tempActionRatio = self.emptyActionDict
        for i in tempActionCount:
            tempActionRatio[i] = tempActionCount[i]/tempTotalActionCount
        print("Action ratio:",tempActionRatio)
        return tempActionRatio

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
        print("Agent performed",action,"action\n")

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

    def getIntentions(self,canCheck, canCall, canRaise):
        canCallOrCheck = canCheck or canCall
        
        bluff = self.predictBluff()

        community = "diff"
        if self.table.communityCard.getName() == self.currentCard.getName():
            community = "same"
        elif self.table.communityCard.getName() == "null":
            community = "null"

        #print("Should:",self.table.currentRound,self.currentCard.getName(),canCallOrCheck,canRaise,bluff,community)
        intentions = self.intentionClass.findIntentions(self.table.currentRound,self.currentCard.getName(),canCallOrCheck,canRaise,bluff,community)
        return intentions

    def predictBluff(self):
        return "null"
        



