##objects
class Card:
    def __init__(self,value):
        self.value = value
        #print("card constructed")

    def __str__(self):
        return f"{self.value}"

class Deck:
    def __init__(self):
        self.values = ["Jack","Queen","King"]
        self.cards = self.makeDeck(2,self.values)
        #print("deck constructed")

    def makeDeck(self, suits, values):
        cards = []
        for suit in range(suits):
            for value in range(len(values)):
                cards.append(Card(values[value-1]))
        return cards

    def printDeck(self):
        print("Cards:")
        for i in self.cards:
            print(i)

class Player:
    def __init__(self,startingBalance, name):
        self.balance = startingBalance
        self.currentCard = Card(-1)
        self.name = name
        self.actions = ["Call","Raise","Fold","Check"]
        #print("player constructed")

    def getBalance(self):
        return self.balance
    
    def getName(self):
        return self.name
    
    def dealCard(self,card):
        currentCard = card

    def availableFunds(self,amount):
        if (amount > self.balance):
            print("Not enough funds in ",self.name,"'s bankroll")
            return False
        else:
            return True

    def changeFunds(self, amount):
        print(self.name, " Balance: ", self.balance)
        self.balance += amount
        print("Amount: ", amount)
        print("New balance: ", self.balance)

##global attributes
p1 = Player(1000,"1")
p2 = Player(2000, "2")
players = [p1,p2]
roundOfPlay = 0
betAmount = 2
pot = 0
turn = 0

deck = Deck()
deck.printDeck()

running = True
while running:
    if roundOfPlay == 0:
        print("\nStart of game:")
        print(players[0].getName() + "'s starting bankroll: ",players[0].getBalance())
        print(players[1].getName() + "'s starting bankroll: ",players[1].getBalance())
        roundOfPlay += 1
    elif roundOfPlay == 1:
        playersWithAvailableFunds = 0
        for player in players:
            if running and player.availableFunds(betAmount) != True:
                running = False
        if running:
            for player in players:
                player.changeFunds(-betAmount)
            ####deal crads to players here
            ####then betting
            roundOfPlay += 1
    elif roundOfPlay == 2:
        roundOfPlay += 1
        ####deal public card here
        ####then betting
    else:
        print("Evaluation")
        ####same value as public card wins
        ####if neither same, highest wins
        running = False

print("End")