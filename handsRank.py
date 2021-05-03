# function rank(), when provided 5 Card(int, int) return the rank of the poker hand from 10 to 1
# Card(int, int) must be provided a integer from 0 to 12 representing from Ace to King and
# a integer from 0 to 3 representing the 4 colors
# rank() is assuming that all the cards are different from a normal deck of 52


class Card(object):
    COLORS = ["Diamonds", "Hearts", "Spades", "Clubs"]
    CARDRANKS = ["Ace"] + list(range(2, 11)) + ["Jack", "Queen", "King"]

    def __init__(self, cardRank=0, color=0):
        """
        :param cardRank: int between 0 and 12
        :param color: int between 0 and 3
        """
        self.color = self.COLORS[color]
        self.colorNum = color
        self.cardRank = self.CARDRANKS[cardRank]
        self.cardNum = cardRank
        self.name = "{} of {}".format(self.cardRank, self.color)


def rank(allCards):
    """
    assume that all the cards are different from a normal deck of 52

    :param allCards: must be a list of 5 Card(int,int)
    :return: the value of rank of the hand
    """

    ROYAL_FLUSH = 1
    STRAIGHT_FLUSH = 2
    FOUR_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 6
    THREE_KIND = 7
    TWO_PAIR = 8
    SINGLE_PAIR = 9
    HIGHEST = 10

    if not len(allCards) == 5:
        raise ValueError("you must use 5 instance of Card")
    for card in allCards:
        if not isinstance(card, Card):
            raise ValueError("{} is not an instance of Card()".format(card))

    currentRank = HIGHEST

    # how many card similar 2,2-2,3,2-3,4 > rank9, 8, 7, 4, 3
    allCardRank = [e.cardRank for e in allCards]
    # store all the same card number in a dictionary
    cardDict = {i: allCardRank.count(i) for i in allCardRank}
    listSameValue = list(cardDict.values())
    if listSameValue.count(2) == 1:
        currentRank = SINGLE_PAIR
    if listSameValue.count(2) == 2:
        currentRank = TWO_PAIR
    if 3 in listSameValue:
        currentRank = THREE_KIND
    if 2 in listSameValue and 3 in listSameValue:
        currentRank = FULL_HOUSE
    if 4 in listSameValue:
        currentRank = FOUR_KIND

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
        currentRank = STRAIGHT

    # does the 5 card has the same color ? > rank5
    hasSameColor = False
    allCardColor = [e.colorNum for e in allCards]
    if allCardColor.count(allCardColor[0]) == 5:
        hasSameColor = True
        currentRank = FLUSH

    # if consecutive order and 5 same colors, does it include the Ace and King? rank 2 and 1
    if isSorted and hasSameColor:
        currentRank = STRAIGHT_FLUSH
        if 12 in allCardNum and 0 in allCardNum:
            currentRank = ROYAL_FLUSH

    return currentRank
