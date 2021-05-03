# function rank(), when provided 5 Card(int, int) return the rank of the poker hand from 10 to 1
# Card(int, int) must be provided a integer from 0 to 12 representing from Ace to King and
# a integer from 0 to 3 representing the 4 colors
# rank() is assuming that all the cards are different from a normal deck of 52

class Card(object):
    def __init__(self, cardRank=0, color=0):
        """
        :param cardRank: int between 0 and 12
        :param color: int between 0 and 3
        """
        self.colors = ["Diamonds", "Hearts", "Spades", "Clubs"]
        self.cardRanks = ["Ace"] + list(range(2, 11)) + ["Jack", "Queen", "King"]
        self.color = self.colors[color]
        self.colorNum = color
        self.cardRank = self.cardRanks[cardRank]
        self.cardNum = cardRank
        self.name = "{} of {}".format(self.cardRank, self.color)


def rank(cardA, cardB, cardC, cardD, cardE):
    """
    assume that all the cards are different from a normal deck of 52

    :param cardA: Class Card(int,int)
    :param cardB: Class Card(int,int)
    :param cardC: Class Card(int,int)
    :param cardD: Class Card(int,int)
    :param cardE: Class Card(int,int)
    :return: int
    """
    # print("your hand is {}, {}, {}, {} and {}".format(cardA.name, cardB.name, cardC.name, cardD.name, cardE.name))
    allCards = [cardA, cardB, cardC, cardD, cardE]
    currentRank = 10

    # how many card similar 2,2-2,3,2-3,4 > rank9, 8, 7, 4, 3
    allCardRank = [e.cardRank for e in allCards]
    # store all the same card number in a dictionary
    cardDict = {i: allCardRank.count(i) for i in allCardRank}
    listSameValue = list(cardDict.values())
    if listSameValue.count(2) == 1:
        currentRank = 9
    if listSameValue.count(2) == 2:
        currentRank = 8
    if 3 in listSameValue:
        currentRank = 7
    if 2 in listSameValue and 3 in listSameValue:
        currentRank = 4
    if 4 in listSameValue:
        currentRank = 3

    # is it in consecutive order ? > rank6. Ace is a special Case where it could be considered as 1 and also top card
    isSorted = False
    allCardNum = [e.cardNum for e in allCards]
    if sorted(allCardNum) == list(range(min(allCardNum), max(allCardNum) + 1)) or sorted(allCardNum) == [
        0,
        9,
        10,
        11,
        12,
    ]:
        isSorted = True
        currentRank = 6

    # does the 5 card has the same color ? > rank5
    hasSameColor = False
    allCardColor = [e.colorNum for e in allCards]
    if allCardColor.count(allCardColor[0]) == 5:
        hasSameColor = True
        currentRank = 5

    # if consecutive order and 5 same colors, does it include the Ace and King? rank 2 and 1
    if isSorted and hasSameColor:
        currentRank = 2
        if 12 in allCardNum and 0 in allCardNum:
            currentRank = 1

    return currentRank
