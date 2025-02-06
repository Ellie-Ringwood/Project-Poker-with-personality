from player import Player

class Agent(Player):
   # def __init__(self):
    #    print("bot constructed")
    #    self.threshhold = 0

    def chooseAction(self, canCheck, canCall, canRaise):
        return "FOLD"

    def bet(self):
        print("")
        print (self.name, "'s turn to bet:")
        print ("Pot:", table.getPot())
        print ("Balance:", self.balance)
        print("Card:",self.currentCard.getName())
        action = ""
        diff = self.getDifference()
        
        canCall = False
        canCheck = False
        canRaise = False

        if (self.amountBetThisRound < table.getCurrentBet()): ## if bets not equal, needs to call to get to same amount
            if (self.balance >= diff): ##if has enough funds to call
                print(" - Call(",diff,")")
                canCall = True
        else:
            print(" - Check")
            canCheck = True
        
        if (self.timesRaisedThisRound < table.maxRaisesEach): ## if not past max bets, can raise
            if(self.balance >= diff + table.raiseAmount):
                print(" - Raise (",diff + table.raiseAmount,")")
                canRaise = True

        print(" - Fold")
        action = self.chooseAction(canCheck, canCall, canRaise)

        match action:
            case "CALL": # add to pot, matching check or raise
                self.removeFunds(diff)
            case "RAISE": # raise by raise amount + any difference to previous player
                self.removeFunds(diff + table.raiseAmount)
                table.addCurrentBet(table.raiseAmount)
                self.timesRaisedThisRound += 1
            case "FOLD": # if everyone but one player folds, they automatically win the hand
                self.folded = True
                table.playerFolds(self)

        

    def handEval(self):
        #
        # if()
        print("hand eval")

    def turn(self):
        #if
        print("turn")




