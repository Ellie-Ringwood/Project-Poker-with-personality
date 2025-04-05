from abc import ABCMeta
from http.client import PARTIAL_CONTENT
from sqlite3 import DateFromTicks
from DeckClass import Deck
import csv

class SituationGenerator():
    def __init__(self):     
        self.possibleCards = Deck(1).cards
        self.rounds = 2
        self.scoreOrder = ["TA","TP","LA", "LP"]
        
    def stringArrayToTypeArray(self, array):
        typeArray = []
        for string in array:
            string = string.strip("' '")
            try:
                correct = int(string)
            except ValueError:
                try:
                    correct = float(string)
                except ValueError:
                    if string == "True":
                        correct = True
                    elif string == "False":
                       correct = False
                    else:
                       correct = string
            typeArray.append(correct)
        if len(typeArray) == 1:
            return typeArray[0]
        else:
            return typeArray

    def setFromFile(self, filename):
        intentions = []
        try:
            f = open(str(filename+".txt"), "r")
        except:
            self.setToFile(filename,1)#
            f = open(str(filename+".txt"), "r")
        for line in f:
            line = line.strip()
            intention = []
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
                                intention.append(self.stringArrayToTypeArray(array))
                            case 2:
                                intention.append(self.stringArrayToTypeArray(array))
                        count += 1
            intentions.append(intention)
        #self.displayArray(intentions)
        return intentions

    def setToFile(self, filename, numberOfScores):
        situations = self.createSituations()
        #self.findRepeats(situations)
        intentions = self.createIntentions(situations, numberOfScores)
        #self.findRepeats(intentions)
        f = open(str(filename+".txt"), "w")
        for intention in intentions:
            f.write(f"{intention}\n")
        f.close()
        
    def addSituation(self,situations,roundNum, card, callCheckFund, canRaise, bluffBelief, communityCard):
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
        
        if (situation not in situations):
            return situations.append(situation)

    def createSituations(self):
        situations = []
        for roundNum in range(1, self.rounds+1):
            for firstBetRound in range(0,2):
                for card in self.possibleCards:
                    for enoughForCallCheck in range(0,2):
                        for canRaise in range(0,2):
                            if roundNum == 1: ## if first round, no community card
                                if firstBetRound == 0: # first bet so can't guess bluff
                                    self.addSituation(situations,roundNum,card,enoughForCallCheck,canRaise,-1,-1)
                                else:
                                    for bluffBelief in range(0,2): #true or false, if agent believes opponent is bluffing 
                                        self.addSituation(situations,roundNum,card,enoughForCallCheck,canRaise,bluffBelief,-1)
                            else: ## not first round
                                for communityCard in range(0,2):
                                    if firstBetRound == 0: # first bet so can't guess bluff
                                        self.addSituation(situations,roundNum,card,enoughForCallCheck,canRaise,-1,communityCard)
                                    else:
                                        for bluffBelief in range(0,2): #true or false, if agent believes opponent is bluffing 
                                            self.addSituation(situations,roundNum,card,enoughForCallCheck,canRaise,bluffBelief,communityCard)
        return situations         

    def findRepeats(self, array):
        newArray = []
        for element in array:
            if element not in newArray:
                newArray.append(element)
        print(len(array)-len(newArray),"repeated elements")

    def createIntentions(self, situations, numberOfScores):
        profileScores = []
        intentions = []
        for i in range(numberOfScores):
            profileScores.append(0)
        for situation in situations:
            possibleActions = self.getPossibleActions(situation)
            for action in possibleActions:
                intentions.append([situation, profileScores, action])
                
        return intentions

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
            
    def findIntentions(self,intentions, roundNum, cardName, callCheckFund, canRaise, bluffBelief, communityCard):
        if roundNum == 1:
            communityCard = "null"
            
        validIntentions = []
        for intention in intentions:
            situation = intention[0]
            
            if (roundNum == situation[0]) or (situation[0] == "any"):
                if (cardName == situation[1]) or (situation[1] == "any"):
                    if (callCheckFund == situation[2]):
                        if(canRaise == situation[3]) or (situation[3] == "any"):
                            if(bluffBelief == situation[4]) or (situation[4] == "any"):
                                if(communityCard == situation[5]) or (situation[5] == "any"):
                                    validIntentions.append(intention)
                                    

        #for intention in validIntentions:
        #   print(intention)
        return validIntentions
    
   # def createCustomProfile(self, ):
        


s = SituationGenerator()
s.setToFile("Ellie", 1)
#s.setToFile()
#print(len(s.situations))
#print(len(s.intentions))
#s.setFromFile()


