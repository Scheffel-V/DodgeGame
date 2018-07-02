import config
import rectangle
import pygame

class Player(rectangle.Rectangle):
    def __init__(self, id, position, width, height, imageOption):
        image = config.PLAYER_IMAGE[imageOption]
        super(Player, self).__init__(position, width, height, image)
        self._isAlive = True
        self._id = id
        self._lastPositions = [[0, 0], [0,0], [0,0], [0,0]]
        self._bomb = None
        self._haveBomb = False

    def kill(self, dodgeGame):
        self._isAlive = False
        dodgeGame.killPlayer(self)

    def isAlive(self):
        return self._isAlive

    def isColliding(self, enemiesList):
        for enemieAux in enemiesList:
            if self.collide(enemieAux):
                return True
        return False

    def getId(self):
        return self._id

    def setLastPositions(self, lastPositions):
        self._lastPositions = lastPositions

    def getLastPositions(self):
        return self._lastPositions

    def getMeanPosition(self):
        lastPositions = self._lastPositions
        meanX = (lastPositions[0][0] + lastPositions[1][0] + lastPositions[2][0] + lastPositions[3][0]) / 4
        meanY = (lastPositions[0][1] + lastPositions[1][1] + lastPositions[2][1] + lastPositions[3][1]) / 4
        return (meanX, meanY)

    def addNewLastPosition(self, newPosition):
        lastPositions = self._lastPositions
        lastPositions[3][0] = lastPositions[2][0]
        lastPositions[3][1] = lastPositions[2][1]
        lastPositions[2][0] = lastPositions[1][0]
        lastPositions[2][1] = lastPositions[1][1]
        lastPositions[1][0] = lastPositions[0][0]
        lastPositions[1][1] = lastPositions[0][1]
        lastPositions[0][0] = newPosition[0]
        lastPositions[0][1] = newPosition[1]
        self.setPosition(self.getMeanPosition())

    def catchBomb(self, bomb):
        self._bomb = bomb
        self._haveBomb = True

    def haveBomb(self):
        return self._haveBomb

    def explodeBomb(self, dodgeGame):
        if self.haveBomb():
            self._bomb.explode(dodgeGame, self.getPosition())
            self._bomb = None
            self._haveBomb = False
