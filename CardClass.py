class Card:
    def __init__(self,value, name):
        self.value = value
        self.name = name
        #print("card constructed")

    def getValue(self):
        return self.value
    
    def getName(self):
        return self.name

    def __str__(self):
        return f"{self.value}"




