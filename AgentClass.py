from PlayerClass import Player
from CardClass import Card
import random
import math

class Agent(Player):
    def __init__(self,table, startingBalance, name, profile):
        ## use player constructor
        super().__init__(table, startingBalance, name)
        ## if using a normal profile (TA,TP,LA,LP) use intentions.txt or if using custom use different file
        if (profile == "TA" or profile == "TP" or profile == "LA", profile == "LP"):
            fileName = "Intentions"
        else:
            fileName = profile
        
        ## create intentions array from the file
        self.intentions = self.table.intentionClass.setFromFile(fileName)

        self.profiles = self.table.intentionClass.scoreOrder
        
        ## check-call-raise-fold ratios for each profile
        self.targetActionRatios = [{"check":0.6,"call":0.6, "raise":0.6, "fold":0.2}, ## adapted for mine
                                   {"check":0.6,"call":0.5, "raise":0.1, "fold":0.7},
                                   {"check":0.6,"call":0.8, "raise":0.7, "fold":0.2},
                                   {"check":0.6,"call":0.9, "raise":0.6, "fold":0.4}]
                                   #{"check":0.6,"call":0.6, "raise":0.6, "fold":0.3},] #check-call-raise-fold ratios for each profile
        
        self.emptyActionDict = {"check":0,"call":0, "raise":0, "fold":0}
        ## profile and target action ratio of this agent
        self.profile = profile
        self.targetActionRatio = self.emptyActionDict.copy()
        ## set target action ratio to the same as its profile's
        for i in range(len(self.profiles)):
            if self.profile == self.profiles[i]:
                self.targetActionRatio = self.targetActionRatios[i]
        
        ## set action count array and total count to be zero
        self.resetActionCount()
        #print("bot constructed")

    def resetHand(self):
        self.currentCard = Card(-1,"null")
        self.folded = False
        self.amountBetThisRound = 0
        self.timesRaisedThisRound = 0
        ## resets action ratio count after each hand (as the difference made will become less impacting as more hands are played)
        self.resetActionCount()

    def resetActionCount(self):
        self.actionCount = {"check":0,"call":0, "raise":0, "fold":0}
        self.totalActionCount = 0
          
    def chooseAction(self):
        ## get intentions for the current situation
        intentions = self.getIntentions()
        
        # get scores for each intention in the intetnions array -> for this profile
        intentionPreference =  self.emptyActionDict.copy()
        for intention in intentions:
            action = intention[2]
            scores = intention[1]
            action = self.getTrueAction(action)

            score = 0
            for i in range(len(self.profiles)):
                if(self.profiles[i] == self. profile):
                    score = scores[i]
            intentionPreference[action] = score 
        print(intentionPreference)

        ## get preference to action based on action ratios
        ## get discrepancy between current action ratio and target
        originalDisc = self.getDiscrepency(self.actionCount, self.targetActionRatio, self.totalActionCount) 
        improvement = self.emptyActionDict.copy()
        
        self.totalActionCount += 1
        ## for each intention, get improvement to action ratio (getting closer to target) caused by the action
        for intention in intentions:
            action = intention[-1]
            action = self.getTrueAction(action)
                    
            tempActionCount = self.actionCount.copy()
            for i in tempActionCount:
                if i == action:
                    tempActionCount[i] += 1
            ## get discrepancy between action ratio after this action and the target ratio
            actionDisc = self.getDiscrepency(tempActionCount, self.targetActionRatio, self.totalActionCount)
            ## get difference between the original discrepency and the discrepancy after each action
            ## positive means its improved overall and negative means its pushed the action ratio away from the target
            improvement[action] = round(originalDisc - actionDisc, 3)
        print(improvement)
        
        decisionScores = self.emptyActionDict.copy()
        for i in intentionPreference:
            # for each action, add the scores from the intention file and the action ratio improvement to get the decision score
            decisionScores[i] = round(intentionPreference[i] + improvement[i],3) #+ (random.randint(0,3)/10), 3)
        print(decisionScores)

        ## pick the best action based on highest decision score, allow for multiple of same value
        bestScore = -10 
        bestActions = []
        for action in decisionScores:
            if (decisionScores[action] > bestScore):
                bestScore = decisionScores[action]
                bestActions = [action]
            elif (decisionScores[action] == bestScore):
                bestActions.append(action)
            
        ## if more than one acvtion with same best score, pick randomly
        if(len(bestActions) == 0):
            chosenAction = bestActions[0]
        else:
            chosenAction = bestActions[random.randint(0,len(bestActions)-1)]           
        
        ## increase action count for chosen action
        for i in self.actionCount:
            if i == chosenAction:
                self.actionCount[i] += 1
        
        chosenAction = self.getTrueAction(chosenAction)
        
        ## show to researcher and allow to type
        print("\n chosen action:",chosenAction)
        input("Faff: ")

        return chosenAction
    
    def getIntentions(self):
        ## pass in the current situation to find the intentions for that situation
        canCallOrCheck = self.canCheck or self.canCall
        
        bluff = self.predictBluff()

        community = "diff"
        if self.table.communityCard.getName() == self.currentCard.getName():
            community = "same"
        elif self.table.communityCard.getName() == "null":
            community = "null"
        
        intentions = self.table.intentionClass.findIntentions(self.intentions, self.table.currentRound,self.currentCard.getName(),canCallOrCheck,self.canRaise,bluff,community)
        return intentions

    def predictBluff(self):
        ## would have been expanded
        return "null"
    
    def getTrueAction(self, action):
        if (action == "call/check"):
            if self.canCall == True:
                action = "call"
            elif self.canCheck == True:
                action = "check"   
        return action
    
    def getDiscrepency(self, current, target, total):
        ## This function is used to calculate how much a array is different from a target array
        discrepency = 0
        
        diff = self.emptyActionDict.copy()
        ## for each action, divide by total to get a decimal
        ## then get the difference between the decimal and the target for that action (magnitude)
        for i in current:
            try:
                value = current[i] / total
            except:
                value = 0
            diff[i] = math.sqrt(pow(value-target[i],2))
        
        ## discrepency is the sum of the differences for all of the actions
        for i in diff:
           discrepency += diff[i]
        return discrepency
    
    def getTrueAction(self, action):
        if (action == "call/check"):
            if self.canCall == True:
                action = "call"
            elif self.canCheck == True:
                action = "check"   
        return action