from PlayerClass import Player
from CardClass import Card
from Situations import SituationGenerator
import time
import random
import copy
import math

class Agent(Player):
    def __init__(self,table, startingBalance, name):
        super().__init__(table, startingBalance, name)
        self.intentions = self.table.intentionClass.setFromFile("Intentions")
        #self.resetHand()
        self.canCall = False
        self.canCheck = False
        self.canRaise = False

        self.profiles = self.table.intentionClass.scoreOrder
        #self.targetActionRatios = [[0.9, 0.6, 0.4, 0.5],[0.6, 0.5, 0.1, 0.7],[0.6, 0.8, 0.7, 0.2],[0.6, 0.9, 0.6, 0.4]] #check-call-raise-fold ratios for each profile
        self.targetActionRatios = [{"check":0.9,"call":0.6, "raise":0.4, "fold":0.5},
                                   {"check":0.6,"call":0.5, "raise":0.1, "fold":0.7},
                                   {"check":0.6,"call":0.8, "raise":0.7, "fold":0.2},
                                   {"check":0.6,"call":0.9, "raise":0.6, "fold":0.4}] #check-call-raise-fold ratios for each profile
        
        self.profile = "LP"
        self.targetActionRatio = {"check":0,"call":0, "raise":0, "fold":0}
        for i in range(len(self.profiles)):
            if self.profile == self.profiles[i]:
                self.targetActionRatio = self.targetActionRatios[i]
        
        self.emptyActionDict = {"check":0,"call":0, "raise":0, "fold":0}
        self.actionCount = self.emptyActionDict.copy()
        self.totalActionCount = 0
        print(self.targetActionRatio)
        #print("bot constructed")

    def chooseAction(self, canCheck, canCall, canRaise):
        intentions = self.getIntentions(canCheck, canCall, canRaise)
        
        # get score for this profile from each action    
        intentionPreference =  self.emptyActionDict.copy()
        for intention in intentions:
            action = intention[2]
            scores = intention[1]
            
            if (action == "call/check"):
                if self.canCall == True:
                    action = "call"
                elif self.canCheck == True:
                    action = "check"

            score = 0
            for i in range(len(self.profiles)):
                if(self.profiles[i] ==self. profile):
                    score = scores[i]
            intentionPreference[action] = score 
        #print(intentionPreference)

        # get preference to action based on action ratios
        originalDisc = self.getDiscrepency(self.actionCount, self.targetActionRatio, self.totalActionCount) ## discrepancy between current action ratio and target
        improvement = self.emptyActionDict.copy()
        for intention in intentions:
            action = intention[-1]
            
            if (action == "call/check"):
                if self.canCall == True:
                    action = "call"
                elif self.canCheck == True:
                    action = "check"
                    
            tempActionCount = self.actionCount.copy() ## needed to copy so as not to change it
            for i in tempActionCount:
                if i == action:
                    tempActionCount[i] += 1
            tempTotalActionCount = self.totalActionCount + 1
            actionDisc = self.getDiscrepency(tempActionCount, self.targetActionRatio, tempTotalActionCount)
            improvement[action] = round(originalDisc - actionDisc, 3) 
            
        #print(improvement)
        
        decisionScores = self.emptyActionDict.copy()
        for i in intentionPreference:
           # print(i, intentionPreference[i], improvement[i],  intentionPreference[i] + improvement[i])
            decisionScores[i] = round(intentionPreference[i] + improvement[i],3) #+ (random.randint(0,3)/10), 3)
        print(decisionScores)

        bestScore = -10 
        bestActions = []
        for action in decisionScores:
            if (decisionScores[action] > bestScore):
                bestScore = decisionScores[action]
                bestActions = [action]
            elif (decisionScores[action] == bestScore):
                bestActions.append(action)
        
        #print(bestAction, best)
        
        print("Waiting for agent decision", end="", flush = True)
        for i in range(random.randint(4,10)):
            print(".", end="")
            time.sleep(0.5)
            
        if(len(bestActions) == 0):
            ChosenAction = bestActions[0]
        else:
            ChosenAction = bestActions[random.randint(0,len(bestActions)-1)]           
        
        for i in self.actionCount:
            if i == ChosenAction:
                self.actionCount[i] += 1
        self.totalActionCount += 1

        """
        #pick random intention
        rand = random.randint(0,len(intentions)-1)
        chosenIntention = intentions[rand]
        #print(chosenIntention)
        action = chosenIntention[2]
        """  
        
        return ChosenAction
    
    def getDiscrepency(self, current, target, total):
        discrepency = 0
        
        #ratio = self.emptyActionDict.copy()
        diff = self.emptyActionDict.copy()
        for i in current:
            try:
                value = current[i] / total
            except:
                value = 0
            #print("i:", i, value)
            diff[i] = math.sqrt(pow(value-target[i],2))
            #print(diff[i])
            
        for i in diff:
           discrepency += diff[i]
        return discrepency

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

        intentions = self.table.intentionClass.findIntentions(self.intentions, self.table.currentRound,self.currentCard.getName(),canCallOrCheck,canRaise,bluff,community)
        return intentions

    def predictBluff(self):
        return "null"
        



