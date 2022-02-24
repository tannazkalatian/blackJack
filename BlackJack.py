import random
from time import sleep

RANKS = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
CARDS_NAMES = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')


class Table:

    def __init__(self, numPlayers):

        self.numPlayers = numPlayers
        self.players = []
        self.dealer = Dealer()
        self.setup()

    def setup(self):
        self.dealer = Dealer()
        for i in range(self.numPlayers):
            self.players.append(Player(i))

    def getPlayers(self):
        return self.players

    def play(self):
        # first round
        for player in self.getPlayers():
            player.hit(self.dealer.giveCard())
            player.hit(self.dealer.giveCard())

        self.dealer.hit(self.dealer.giveCard())

        round = 1
        while (self.dealer.getValue() < 17):
            print('********************** Round: ' + str(round) + " **********************")

            for playerNum, player in enumerate(self.getPlayers()):
                if player.isBusted() or player.isWinner():
                    continue
                print(player.showDetail())
                response = input("\t Hit or Stay?")
                # print(value)
                if response.lower() == "hit":
                    player.hit(self.dealer.giveCard())
                    print(player.showDetail())

            self.dealer.hit(self.dealer.giveCard())
            print(self.dealer.showDetail())

            winners = self.judge()
            for winner in winners:
                print(winner.showDetail())
            sleep(1)
            round = round + 1

        self.judge()
        for p in self.players:
            print(p.showDetail())

    def judge(self):
        winners = []
        for playerNum, player in enumerate(self.getPlayers()):
            if player.isBusted() or player.isWinner():
                continue
            if player.getValue() == 21:
                winners.append(player)
                player.setWinner(True)

        if self.dealer.getValue() >= 17 and self.dealer.getValue() < 21:
            for playerNum, player in enumerate(self.getPlayers()):
                if player.isBusted() or player.isWinner():
                    continue
                if player.getValue() > self.dealer.getValue():
                    winners.append(player)
                    player.setWinner(True)

        return winners


class Player:
    def __init__(self, num):
        self.hand = Hand()
        self.num = num
        self.busted = False
        self.winner = False

    def isWinner(self):
        return self.winner

    def setWinner(self, newStatus):
        self.winner = newStatus

    def isBusted(self):
        return self.busted

    def hit(self, newCard):
        self.hand.addCard(newCard)
        if (self.getValue() > 21):
            self.busted = True
        if (self.getValue() == 21):
            self.setWinner(True)

    def showDetail(self):
        return 'Player: ' + str(self.num) + " \t Current hand -> " + self.hand.show() + " Total value -> " + str(
            self.getValue()) + " isbusted: " + str(self.busted) + " --isWinner: " + str(self.winner)

    def getValue(self):
        return self.hand.getValue()

    # def checkStatus(self):
    # currentValue = hand.getValue()
    # if currentValue == 21:


class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.cards = []
        for cardName in CARDS_NAMES:
            self.cards.append(Card(cardName))
            self.cards.append(Card(cardName))
            self.cards.append(Card(cardName))
            self.cards.append(Card(cardName))
        self.shuffle()

    def giveCard(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

    def hit(self, newCard):
        self.hand.addCard(newCard)

    # def checkStatus():
    # pass
    def showDetail(self):
        return 'Dealer: ' + " \t Current hand -> " + self.hand.show() + " Total value -> " + str(self.getValue())

    def shuffle(self):
        random.shuffle(self.cards)

    def getValue(self):
        return self.hand.getValue()


class Hand:
    def __init__(self):
        self.cards = []

    def addCard(self, newCard):
        self.cards.append(newCard)

    def getValue(self):
        value = 0
        for card in self.cards:
            value += card.getValue()
        return value

    def show(self):
        currentHand = ""
        for card in self.cards:
            currentHand += card.getName() + " "
        return currentHand.strip()


class Card:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getValue(self):
        return RANKS[self.getName()]


def main():
    t1 = Table(2)
    t1.play()

main()
