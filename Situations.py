from abc import ABCMeta
from DeckClass import Deck

class SituationGenerator():
    def __init__(self):
        self.situations = []
        self.intentions = []        
        self.possibleCards = Deck(1).cards
        self.rounds = 2

    def setFromFile(self):
        print("set from file")
        if self.intentions == []:
            f = open("Intentions.txt", "r")
            for line in f:
                line = line.strip()
                for word in line.strip('[]').split(','):
                    print(word)
                
                self.intentions.append(line.strip())
        #self.displayArray(self.intentions)

    def setToFile(self):
        self.createSituations()
        self.findRepeats(self.situations)
        self.createIntentions()
        self.findRepeats(self.intentions)
        f = open("Intentions.txt", "w")
        for intention in self.intentions:
            f.write(f"{intention}\n")
        f.close()
        
    def addSituation(self,roundNum, card, callCheckFund, canRaise, bluffBelief, communityCard):
        match communityCard:
            case 0:
                communityCardStatus = "same"
            case 1:
                communityCardStatus = "diff"
            case _:
                communityCardStatus = "null"
                
        if bluffBelief == -1:
            bluffStatus = "null"
        else:
            bluffStatus = bool(bluffBelief)
            
        if(callCheckFund == False) and (canRaise == False):
            situation = ["any","any", bool(callCheckFund), bool(canRaise), "any","any"]
        else:
            situation = [roundNum, card.getName(), bool(callCheckFund), bool(canRaise), bluffStatus, communityCardStatus]
        
        if (situation not in self.situations):
            self.situations.append(situation)

    def createSituations(self):
        for roundNum in range(1, self.rounds+1):
            for firstBetRound in range(0,2):
                for card in self.possibleCards:
                    for enoughForCallCheck in range(0,2):
                        for canRaise in range(0,2):
                            if roundNum == 1: ## if first round, no community card
                                if firstBetRound == 0: # first bet so can't guess bluff
                                    self.addSituation(roundNum,card,enoughForCallCheck,canRaise,-1,-1)
                                else:
                                    for bluffBelief in range(0,2): #true or false, if agent believes opponent is bluffing 
                                        self.addSituation(roundNum,card,enoughForCallCheck,canRaise,bluffBelief,-1)
                            else: ## not first round
                                for communityCard in range(0,2):
                                    if firstBetRound == 0: # first bet so can't guess bluff
                                        self.addSituation(roundNum,card,enoughForCallCheck,canRaise,-1,communityCard)
                                    else:
                                        for bluffBelief in range(0,2): #true or false, if agent believes opponent is bluffing 
                                            self.addSituation(roundNum,card,enoughForCallCheck,canRaise,bluffBelief,communityCard)
         
    def findRepeats(self, array):
        newArray = []
        for element in array:
            if (element not in newArray):
                newArray.append(element)
        print(len(array)-len(newArray),"repeated elements")

    def createIntentions(self):
        profileScores = [0,0]
        outcomeScore = 0
        for situation in self.situations:
            possibleActions = self.getPossibleActions(situation)
            for action in possibleActions:
                self.intentions.append([situation, profileScores, outcomeScore, action]) 

    def displayArray(self,array):
        print(len(array))
        print("Round, card, call/check, raise, bluff, community")
        for element in array:
            print(element)

    def getPossibleActions(self, situation):
        roundNum = situation[0]
        card = situation[1]
        canCallCheck = situation[2]
        canRaise = situation[3]
        bluff = situation[4]
        communityCard = situation[5]
        
        possibleActions = []
        
        if canRaise:
            possibleActions.append("raise")
        if canCallCheck:
            possibleActions.append("call/check")
        possibleActions.append("fold")
        return possibleActions
            
    def findIntentions(self, roundNum, cardName, callCheckFund, canRaise, bluffBelief, communityCard):
        if roundNum == 1:
            communityCard = "null"
        print("Round, card, call/check, raise, bluff, community")
        validIntentions = []
        
        for intention in self.intentions:
            situation = intention[0]
            print(situation)
            if (roundNum == situation[0]) or (situation[0] == "any"):
                print("round")
                if (cardName == situation[1]) or (situation[1] == "any"):
                    if (callCheckFund == situation[2]):
                        if(canRaise == situation[3]):
                            if(bluffBelief == situation[4]) or (situation[4] == "any"):
                                print("bluff")
                                if(communityCard == situation[5]) or (situation[5] == "any"):
                                    validIntentions.append(intention)

        for intention in validIntentions:
            print(intention)   

#s = SituationGenerator()
#s.setToFile()
#s.setFromFile()



