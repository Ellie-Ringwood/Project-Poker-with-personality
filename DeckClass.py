import random
from CardClass import Card

class Deck:
    def __init__(self,suits):
        self.values = ["Jack","Queen","King"]
        self.cards = self.makeDeck(suits,self.values)
        #print("deck constructed")

    def makeDeck(self, suits, values):
        cards = []
        for suit in range(suits):
            for value in range(len(values)):
                cards.append(Card(value,values[value]))
        return cards

    def printDeck(self):
        print("Cards:")
        for i in self.cards:
            print(i)

    def shuffleDeck(self):
        tempCards = []
        while (len(self.cards) > 0):
            randNum = random.randrange(0, len(self.cards))
            tempCards.append(self.cards[randNum])
            self.cards.pop(randNum)
        self.cards = tempCards

    def dealCard(self):
        card = self.cards.pop()
        #print(card)
        return card

    def dealSpecificCard(self, cardValue):
        for card in self.cards:
            if card.getName() == cardValue:
                self.cards.remove(card)
                return card




