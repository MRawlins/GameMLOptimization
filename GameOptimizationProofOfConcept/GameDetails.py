import random

class Card:
    def __init__(self, isDanger: bool, dangerValue: int, isIdol: bool, gemValue: int):
        self.isDanger = isDanger
        self.dangerValue = dangerValue
        self.isIdol = isIdol
        self.gemValue = gemValue

class Deck:
    def __init__(self):
        self.cardList = []
        #Add danger cards
        for dangerValue in range(5):
           for x in range(3):
               self.cardList.append(Card(True, dangerValue, False, -1))
        #Add Idols
        for x in range(5):
            self.cardList.append(Card(False, -1, True, 5))
        #Add rest of cards
        self.cardList.append(Card(False, -1, False, 1))
        self.cardList.append(Card(False, -1, False, 2))
        self.cardList.append(Card(False, -1, False, 3))
        self.cardList.append(Card(False, -1, False, 4))
        self.cardList.append(Card(False, -1, False, 5))
        self.cardList.append(Card(False, -1, False, 5))
        self.cardList.append(Card(False, -1, False, 7))
        self.cardList.append(Card(False, -1, False, 7))
        self.cardList.append(Card(False, -1, False, 9))
        self.cardList.append(Card(False, -1, False, 11))
        self.cardList.append(Card(False, -1, False, 11))
        self.cardList.append(Card(False, -1, False, 13))
        self.cardList.append(Card(False, -1, False, 14))
        self.cardList.append(Card(False, -1, False, 15))
        self.cardList.append(Card(False, -1, False, 17))

class Player:
    def __init__(self):
        self.gemsInHand = 0
        self.totalGems = 0
    def reset(self):
        self.totalGems = 0
        self.gemsInHand = 0
    def endRound(self):
        self.totalGems += self.gemsInHand
        self.gemsInHand = 0
    def chooseToContinue(self):
        if(self.gemsInHand == 0):
            return True
        else:
            return random.choice([True, False])

class GameState:
    def __init__(self, players):
        self.players = players
        self.currentPlayers = self.players
        self.gemsOnBoard = 0
        self.dangersOnBoard = 0
        self.currentDangers = []
        self.roundEnd = False
    def reset(self):
        self.currentPlayers = self.players
        self.gemsOnBoard = 0
        self.dangersOnBoard = 0
        self.currentDangers = []
        self.roundEnd = False
        for player in self.players:
            player.reset()
    def update(self, card: Card):
        if(card.isDanger):
            for danger in self.currentDangers:
                if(card.dangerValue == danger):
                    self.roundEnd = True
            self.currentDangers.append(card.dangerValue)
            self.dangersOnBoard += 1
        elif(card.isIdol):
            self.gemsOnBoard += card.gemValue
        else:
            toAdd = card.gemValue // len(self.currentPlayers)
            for player in self.currentPlayers:
                player.gemsInHand += toAdd
            self.gemsOnBoard += card.gemValue % len(self.currentPlayers)

def playRound(gameState: GameState, deck: Deck):
    random.shuffle(deck.cardList)
    for card in deck.cardList:
        leavingPlayers = []
        if(len(gameState.currentPlayers) == 0):
            break
        gameState.update(card)
        #if the round ends, current players lose everything
        if(gameState.roundEnd):
            for player in gameState.currentPlayers:
                player.reset()
            gameState.reset()
            break
        #round continues, players choose whether to stay or go
        for player in gameState.currentPlayers:
            keepGoing = player.chooseToContinue()
            if(not keepGoing):
                leavingPlayers.append(player)
        #remove leaving players from current players
        for player in leavingPlayers:
            gameState.currentPlayers.remove(player)
        #if only one player leaves, he gets all gems
        if(len(leavingPlayers) == 1):
            leavingPlayers[0].gemsInHand += gameState.gemsOnBoard
            gameState.gemsOnBoard = 0
        for player in leavingPlayers:
            player.endRound()
