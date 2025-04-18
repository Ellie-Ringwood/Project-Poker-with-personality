from DeckClass import Deck

class SituationGenerator():
    def __init__(self):
        ## define game
        self.possibleCards = Deck(1).cards
        self.rounds = 2
        self.scoreOrder = ["TA","TP", "LA", "LP"]
        
    def displayArray(self,array):
        print(len(array))
        print("Round, card, call/check, raise, bluff, community")
        for element in array:
            print(element)
        
    def stringArrayToTypeArray(self, array):
        ## take an array of strings (usually from a file) and convert them back to the correct data type
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
        ## try to open file. If doesnt exist, call 'set to file' (create new custom profile)
        try:
            f = open(str(filename+".txt"), "r")
        except:
            self.setToFile(filename,1)
            f = open(str(filename+".txt"), "r")
        ## split up file into lines and lines into individual array elements
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
                        ## convert string back to actual data type
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
        ## generate all possible situations, create intentions for them and set to text file
        situations = self.createSituations()
        intentions = self.createIntentions(situations, numberOfScores)
        f = open(str(filename+".txt"), "w")
        for intention in intentions:
            f.write(f"{intention}\n")
        f.close()

    def createSituations(self):
        ## create unique situations from information such as round number, card in hand, 
        ## what actions are allowed with funds and bluffing beliefs
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
    
    def addSituation(self,situations,roundNum, card, callCheckFund, canRaise, bluffBelief, communityCard):
        ## set community card state (same, different or null)
        match communityCard:
            case 0:
                communityCardStatus = "same"
            case 1:
                communityCardStatus = "diff"
            case _:
                communityCardStatus = "null"
        ## set bluff (true, false or null) 
        if bluffBelief == -1:
            bluffStatus = "null"
        else:
            bluffStatus = bool(bluffBelief)
        ## if cannot call or check, create just one situation as the only option is to fold
        if(callCheckFund == False):
            situation = ["any","any", bool(callCheckFund), "any", "any","any"]
        else:
            situation = [roundNum, card.getName(), bool(callCheckFund), bool(canRaise), bluffStatus, communityCardStatus]
        ## append situation (if unique) to an array of situations
        if (situation not in situations):
            return situations.append(situation)

    def createIntentions(self, situations, numberOfScores):
        ## take situations and create an array of intentions
        ## each element will have a situation array, score array and action
        profileScores = []
        intentions = []
        ## create score array for each profile
        for i in range(numberOfScores):
             profileScores.append(0)
        ## get the possible actions for each situation and append an intention for each action
        for situation in situations:
             possibleActions = self.getPossibleActions(situation)
             for action in possibleActions:
                 intentions.append([situation, profileScores, action])
        return intentions

    def getPossibleActions(self, situation):
        canCallCheck = situation[2]
        canRaise = situation[3]
        
        ## use situation to get what actions are available
        possibleActions = []
        if canRaise and canCallCheck == True:
            possibleActions.append("raise")
        if canCallCheck:
            possibleActions.append("call/check")
        possibleActions.append("fold")
        return possibleActions
            
    def findIntentions(self,intentions, roundNum, cardName, callCheckFund, canRaise, bluffBelief, communityCard):
        ## takes an intention array and situation variables (roundNum, cardName, callCheckFund, canRaise, bluffBelief, communityCard)
        if roundNum == 1:
            communityCard = "null"
            
        ## find intentions with situations which match the passed in situation variables
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
        return validIntentions

"""
## used for individual testing
s = SituationGenerator()
#s.setToFile()
print(len(s.situations))
print(len(s.intentions))
s.setFromFile()
"""


