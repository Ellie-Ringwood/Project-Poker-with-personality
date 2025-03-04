from abc import ABCMeta
from http.client import PARTIAL_CONTENT
from DeckClass import Deck
import csv

class SituationGenerator():
    def __init__(self):
        self.situations = []
        self.intentions = []        
        self.possibleCards = Deck(1).cards
        self.rounds = 2
        
    def stringArrayToTypeArray(self, array):
        typeArray = []
        for string in array:
            string = string.strip("' '")
            try:
                correct = int(string)
                #print("int:", correct)
            except ValueError:
                if string == "True":
                    correct = True
                    #print("bool:",correct)
                elif string == "False":
                   correct = False
                   #print("bool:",correct)
                else:
                   correct = string
                   #print("string:", string)
            typeArray.append(correct)
        if len(typeArray) == 1:
            return typeArray[0]
        else:
            return typeArray

    def setFromFile(self):
        if self.intentions == []:
            f = open("Intentions.txt", "r")
            for line in f:
                line = line.strip()
                intention = []
                scores = []
                count = 0
                for word in line.split('],'):
                    word = word.strip()
                    word = word.strip("]")
                    found = False
                    for i in range(len(word)):
                        if word[i] != "[" and not found:
                            array = word[i:].split(",")
                            found = True
                            match count:
                                case 0:
                                    intention.append(self.stringArrayToTypeArray(array))
                                case 1:
                                    scores.append(self.stringArrayToTypeArray(array))
                                case 2:
                                    scores.append(self.stringArrayToTypeArray(array))
                                    intention.append(scores)
                                case 3:
                                    intention.append(self.stringArrayToTypeArray(array))
                            count += 1
                self.intentions.append(intention)
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
            
        if(callCheckFund == False):
            situation = ["any","any", bool(callCheckFund), "any", "any","any"]
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
            if element not in newArray:
                newArray.append(element)
        print(len(array)-len(newArray),"repeated elements")

    def createIntentions(self):
        profileScores = [0,0,0,0]
        #outcomeScore = 0
        for situation in self.situations:
            possibleActions = self.getPossibleActions(situation)
            for action in possibleActions:
                self.intentions.append([situation, profileScores, action]) 
                #self.intentions.append([situation, [profileScores, outcomeScore], action]) 

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
        
        if canRaise and canCallCheck == True:
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
            
            if (roundNum == situation[0]) or (situation[0] == "any"):
                if (cardName == situation[1]) or (situation[1] == "any"):
                    if (callCheckFund == situation[2]):
                        if(canRaise == situation[3]) or (situation[3] == "any"):
                            if(bluffBelief == situation[4]) or (situation[4] == "any"):
                                if(communityCard == situation[5]) or (situation[5] == "any"):
                                    validIntentions.append(intention)
                                    

        #for intention in validIntentions:
        #    print(intention)
        return validIntentions

s = SituationGenerator()
s.setToFile()
print(len(s.situations))
print(len(s.intentions))
#s.setFromFile()



