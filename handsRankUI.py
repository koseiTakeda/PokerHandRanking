# GUI for handsRank.py done in PyQt5
# handsRankForm.ui : base of the ui done in Designer, converted to handsRankForm.py using pyuic5

import sys

from PyQt5 import QtWidgets, QtCore, QtGui

import handsRank
import handsRankForm


class ListBaseClass(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(ListBaseClass, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setWrapping(True)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.setDragEnabled(False)
        self.setSpacing(0)
        self.setGeometry(9, 9, 800, 400)
        self.listName = ""
        self.setIconSize(QtCore.QSize(70, 100))
        self.setResizeMode(QtWidgets.QListView.Adjust)


class CardListItem(handsRank.Card, QtWidgets.QListWidgetItem):
    def __init__(self, *args, **kwargs):
        # Grab the args as a list so we can edit it
        args = list(args)
        otherNode = args.pop(0)

        # initiate the inherited class
        QtWidgets.QListWidgetItem.__init__(self, *args, **kwargs)

        # Set all necessary attributes that come from the base class if they're present
        self.CARDRANKS = otherNode.CARDRANKS if otherNode else ""
        self.color = otherNode.color if otherNode else ""
        self.colorNum = otherNode.colorNum if otherNode else ""
        self.cardRank = otherNode.cardRank if otherNode else ""
        self.cardNum = otherNode.cardNum if otherNode else ""
        self.name = otherNode.name if otherNode else ""

        backgroundColor = "black"
        if self.color == "Hearts" or self.color == "Clubs":
            backgroundColor = "red"

        # draw of Icon
        xSize = 70
        ySize = 100
        pixmap = QtGui.QPixmap(xSize, ySize)
        pixmap.fill(QtGui.QColor(backgroundColor))

        font = QtGui.QFont("Times", 10)
        metrics = QtGui.QFontMetricsF(font)
        cardRankTxt = str(self.cardRank)
        cardRankRect = metrics.boundingRect(cardRankTxt)
        xPosCardRank = (pixmap.width() - cardRankRect.width()) / 2  # right in the middle
        yPos = pixmap.height() / 2
        ofTxt = "of"
        ofRect = metrics.boundingRect(ofTxt)
        xPosOf = (pixmap.width() - ofRect.width()) / 2
        colorText = str(self.color)
        colorRect = metrics.boundingRect(colorText)
        xPosColor = (pixmap.width() - colorRect.width()) / 2

        painter = QtGui.QPainter()
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.begin(pixmap)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(250, 250, 240))
        painter.drawText(int(xPosCardRank), int(yPos) - 17, cardRankTxt)
        painter.drawText(int(xPosOf), int(yPos), ofTxt)
        painter.drawText(int(xPosColor), int(yPos) + 17, colorText)

        painter.end()

        self.setIcon(QtGui.QIcon(pixmap))

        # self.setTextAlignment(QtCore.Qt.AlignCenter)
        self.setSizeHint(QtCore.QSize(xSize + 0, ySize + 0))


class ColorListItem(QtWidgets.QListWidgetItem):
    def __init__(self, name, colorBackground="white", colorText="black"):
        """
        :param name: str
        :param colorBackground: str
        :param colorText: str
        """
        super().__init__()

        self.name = name

        # draw of Icon
        xSize = 70
        ySize = 100
        pixmap = QtGui.QPixmap(xSize, ySize)
        pixmap.fill(QtGui.QColor(colorBackground))

        font = QtGui.QFont("Times", 10)
        metrics = QtGui.QFontMetricsF(font)
        text = self.name
        rect = metrics.boundingRect(text)
        xPos = (pixmap.width() - rect.width()) / 2  # right in the middle
        yPos = (pixmap.height() - rect.height()) / 2 + 10  # middle
        painter = QtGui.QPainter()
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.begin(pixmap)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(colorText))
        painter.drawText(int(xPos), int(yPos), text)
        painter.drawRect(2, 2, xSize - 6, ySize - 5)
        painter.end()

        self.setIcon(QtGui.QIcon(pixmap))

        # self.setTextAlignment(QtCore.Qt.AlignCenter)
        self.setSizeHint(QtCore.QSize(xSize + 1, ySize + 1))


def handRankText(num):
    text = ""
    if num == 10:
        text = "10. Your highest card is your actual hand"
    elif num == 9:
        text = "9. Congratulation, you have a Single pair!"
    elif num == 8:
        text = "8. Congratulation, you have Two pair!"
    elif num == 7:
        text = "7. Congratulation, you have Three of a kind!"
    elif num == 6:
        text = "6. Congratulation, you have a Straight!"
    elif num == 5:
        text = "5. Congratulation, you have a Flush!!"
    elif num == 4:
        text = "4. Wow! Congratulation, you have a Full House!!"
    elif num == 3:
        text = "3. Wow! Congratulation, you have 4 of a Kind!!!"
    elif num == 2:
        text = "2. AMAZING!! you have a Straight Flush!"
    elif num == 1:
        text = "1. CONGRATULATION! You have A Royal Flush!! you WIN!"
    return text


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # initiate Ui and elements
        self.ui = handsRankForm.Ui_MainWindow()
        self.ui.setupUi(self)

        self.colorListWidget = ListBaseClass()
        self.ui.main_QVB.insertWidget(1, self.colorListWidget)
        self.numberCardListWidget = ListBaseClass()
        self.ui.main_QVB.insertWidget(3, self.numberCardListWidget)
        self.handCardListWidget = ListBaseClass()
        self.ui.main_QVB.insertWidget(5, self.handCardListWidget)

        self.colorListWidget.setMinimumHeight(105)
        self.numberCardListWidget.setMinimumHeight(310)
        self.handCardListWidget.setMinimumHeight(105)

        # storage of current cards in our hand
        self.allHandCards = []

        # populate colors and numbers
        self.colorListWidget.addItem(ColorListItem(name="Diamonds", colorBackground="black", colorText="white"))
        self.colorListWidget.addItem(ColorListItem(name="Hearts", colorBackground="Red", colorText="white"))
        self.colorListWidget.addItem(ColorListItem(name="Spades", colorBackground="black", colorText="white"))
        self.colorListWidget.addItem(ColorListItem(name="Clubs", colorBackground="Red", colorText="white"))

        listCard = handsRank.Card()
        for cardRank in listCard.CARDRANKS:
            self.numberCardListWidget.addItem(ColorListItem(name=str(cardRank)))

        # connecting ui buttons
        self.ui.addCard_btn.clicked.connect(self.addCard)
        self.ui.removeCard_btn.clicked.connect(self.removeCard)

    def addCard(self):
        colorNum = self.colorListWidget.currentRow()
        cardNum = self.numberCardListWidget.currentRow()
        cardToAdd = handsRank.Card(cardNum, colorNum)

        # check if the card is not already in our hand
        if self.allHandCards:
            for cardHand in self.allHandCards:
                if cardToAdd.colorNum == cardHand.colorNum and cardToAdd.cardNum == cardHand.cardNum:
                    self.ui.statusbar.showMessage("{} is already in your hand".format(cardToAdd.name))
                    return

        # remove the last or replace the selected card if we have a full hand
        if len(self.allHandCards) == 5:
            self.removeCard()

        self.handCardListWidget.addItem(CardListItem(cardToAdd))
        self.allHandCards.append(cardToAdd)
        self.ui.statusbar.showMessage("{} added".format(cardToAdd.name))
        self.updateHand()

    def removeCard(self):
        if not self.allHandCards:
            return

        handCardNum = self.handCardListWidget.currentRow()
        self.allHandCards.pop(handCardNum)
        self.handCardListWidget.clear()
        if self.allHandCards:
            for handCard in self.allHandCards:
                self.handCardListWidget.addItem(CardListItem(handCard))
        self.updateHand()

    def updateHand(self):
        if not len(self.allHandCards) == 5:
            self.ui.hands_label.setText(" ")
            return

        deckRank = handsRank.rank(self.allHandCards)
        self.ui.hands_label.setText(handRankText(deckRank))


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainW = MainWindow()
    mainW.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
