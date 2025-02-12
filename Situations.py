from DeckClass import Deck

class SituationGenerator():
    def __init__(self):
        self.situations = []
        self.possibleCards = Deck(1)
        self.rounds = 2
        #for card in self.possibleCards.cards:
        #    print(card)
        self.createSituations()
        self.displaySituations()
        self.findRepeats()
        
        
    def addSituation(self,roundNum, card, callCheckFund, canRaise, bluffBelief, communityCard):
        #print(roundNum,card, callCheckFund, raiseFund, canRaise, bluffBelief, communityCard)
        match communityCard:
            case 0:
                communityCardStatus = "same"
            case 1:
                communityCardStatus = "diff"
            case _:
                communityCardStatus = "none"
                
        if bluffBelief == -1:
            bluffStatus = "none"
        else:
            bluffStatus = bool(bluffBelief)
        
        self.situations.append([roundNum, card, bool(callCheckFund), bool(canRaise), bluffStatus, communityCardStatus])
        
    """
    def createSituations(self):
        for roundNum in range(self.rounds):
            for firstBetRound in range(0,2):
                for card in range(len(self.possibleCards.cards)):
                    for enoughForCallCheck in range(0,2):
                        for enoughForRaise in range(0,2):
                            for canRaise in range(0,2):
                                if roundNum == 0: ## if first round, no community card
                                    communityCard = -1
                                    self.addSituation(card,enoughForCallCheck,enoughForRaise,canRaise,bluffBelief,-1)
                                else:
                                    communityCard = -1
                                for communityCard in range(0,3):
                                    if firstBetRound == 0: # first bet so can't guess bluff
                                        self.addSituation(card,enoughForCallCheck,enoughForRaise,canRaise,-1,communityCard)
                                    else:
                                        for bluffBelief in range(0,2): #true or false, if agent believes opponent is bluffing 
                                            self.addSituation(card,enoughForCallCheck,enoughForRaise,canRaise,bluffBelief,communityCard)
    """
    def createSituations(self):
        for roundNum in range(self.rounds):
            for firstBetRound in range(0,2):
                for card in range(len(self.possibleCards.cards)):
                    for enoughForCallCheck in range(0,2):
                        for canRaise in range(0,2):
                            if roundNum == 0: ## if first round, no community card
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
         

    
    def findRepeats(self):
        newSituations = []
        for situation in self.situations:
            if not(situation in newSituations):
                newSituations.append(situation)
        
        print(len(newSituations))
        #print("Round, card, call/check, raise, bluff, community")
        #for situation in self.situations:
        #    print(situation)



    def displaySituations(self):
        print(len(self.situations))
        print("Round, card, call/check, raise, bluff, community")
        for situation in self.situations:
            print(situation)


SituationGenerator()



