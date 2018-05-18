import rectangle
import dodgegame
import math
import config
import abc
import random

class Enemie(rectangle.Rectangle):
    def __init__(self, position, width, height, image, speed):
        super(Enemie, self).__init__(position, width, height, image)
        self._speed = speed
        self._originalSpeed = speed
        self._target = None

    def getSpeed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def refreshSpeed(self):
        self._speed = self._originalSpeed

    def hit(self, dodgeGame):
        self.despawn(dodgeGame)

    def slow(self, slow):
        if self._speed != 0:
            self._speed -= slow

    def stun(self):
        self._speed = 0

    def setIce(self, iceEffect):
        if not self.isIced():
            self._specialEffects.append(iceEffect)
            self.slow(iceEffect.getSlow())

    def isIced(self):
        for effectAux in self._specialEffects:
            if effectAux.getName() == "Ice":
                return True
        return False

    def setThunder(self, thunderEffect):
        if not self.isStunned():
            self._specialEffects.append(thunderEffect)
            self.stun()

    def isStunned(self):
        for effectAux in self._specialEffects:
            if effectAux.getName() == "Thunder":
                return True
        return False

    def setEffect(self, effect):
        if effect.getName() == "Ice":
            self.setIce(effect)
        elif effect.getName() == "Thunder":
            self.setThunder(effect)

    def delEffect(self, effect):
        if effect.getName() == "Ice":
            self.refreshSpeed()
        elif effect.getName() == "Thunder":
            self.refreshSpeed()
        if self._specialEffects.__contains__(effect):
            self._specialEffects.remove(effect)

    def executeEffects(self):
        for effectAux in self._specialEffects:
            effectAux.decDuration()

    def despawn(self, dodgeGame):
        dodgeGame.killEnemie(self)

    def getTarget(self, dodgeGame):
        players = dodgeGame.getPlayers()
        nearestPlayer = None
        lowestDistance = 999999
        for playerAux in players:
            distance = self.distance(playerAux.getCenter())
            if distance < lowestDistance:
                lowestDistance = distance
                nearestPlayer = playerAux
        return nearestPlayer.getCenter()

    def calculateDirection(self):
        vector = self._target[0] - self._position[0], self._target[1] - self._position[1]
        vector = vector[0], vector[1]
        return self.normalizeVector(vector)

    def normalizeVector(self, vector):
        norma = math.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))  # normalizing
        newX = vector[0] / norma
        newY = vector[1] / norma
        return (newX, newY)

    @abc.abstractmethod
    def getClass(self):
        return

    @abc.abstractmethod
    def move(self, dodgeGame):
        return

class BlueEnemie(Enemie):
    def __init__(self, position):
        super(BlueEnemie, self).__init__(position,
                                           config.ENEMIE_BLUE_WIDTH,
                                           config.ENEMIE_BLUE_HEIGHT,
                                           config.ENEMIE_BLUE_IMAGE_small,
                                           config.ENEMIE_BLUE_SPEED)

    def move(self, dodgeGame):
        self._target = self.getTarget(dodgeGame)
        _direction = self.calculateDirection()
        newPositionX = self._position[0] + (_direction[0] * self._speed)
        newPositionY = self._position[1] + (_direction[1] * self._speed)
        self.setPosition((newPositionX, newPositionY))

    def getClass(self):
        return "BlueEnemie"

class YellowEnemie(Enemie):
    def __init__(self, position):
        super(YellowEnemie, self).__init__(position,
                                           config.ENEMIE_YELLOW_WIDTH,
                                           config.ENEMIE_YELLOW_HEIGHT,
                                           config.ENEMIE_YELLOW_IMAGE_small,
                                           config.ENEMIE_YELLOW_SPEED)

    def move(self, dodgeGame):
        self._target = self.getTarget(dodgeGame)
        _direction = self.calculateDirection()
        newPositionX = self._position[0] + (_direction[0] * self._speed)
        newPositionY = self._position[1] + (_direction[1] * self._speed)
        self.setPosition((newPositionX, newPositionY))

    def getClass(self):
        return "YellowEnemie"

class RedEnemie(Enemie):
    def __init__(self, position):
        super(RedEnemie, self).__init__(position,
                                           config.ENEMIE_RED_WIDTH,
                                           config.ENEMIE_RED_HEIGHT,
                                           config.ENEMIE_RED_IMAGE_small,
                                           config.ENEMIE_RED_SPEED)

    def move(self, dodgeGame):
        self._target = self.getTarget(dodgeGame)
        _direction = self.calculateDirection()
        newPositionX = self._position[0] + (_direction[0] * self._speed)
        newPositionY = self._position[1] + (_direction[1] * self._speed)
        self.setPosition((newPositionX, newPositionY))

    def getClass(self):
        return "RedEnemie"

class GreenEnemie(Enemie):
    def __init__(self, position):
        super(GreenEnemie, self).__init__(position,
                                           config.ENEMIE_GREEN_WIDTH,
                                           config.ENEMIE_GREEN_HEIGHT,
                                           config.ENEMIE_GREEN_IMAGE_small,
                                           config.ENEMIE_GREEN_SPEED)

    def move(self, dodgeGame):
        self._target = self.getTarget(dodgeGame)
        _direction = self.calculateDirection()
        newPositionX = self._position[0] + (_direction[0] * self._speed)
        newPositionY = self._position[1] + (_direction[1] * self._speed)
        self.setPosition((newPositionX, newPositionY))

    def getClass(self):
        return "GreenEnemie"

class PurpleEnemie(Enemie):
    def __init__(self, position):
        super(PurpleEnemie, self).__init__(position,
                                           config.ENEMIE_PURPLE_WIDTH,
                                           config.ENEMIE_PURPLE_HEIGHT,
                                           config.ENEMIE_PURPLE_IMAGE_small,
                                           config.ENEMIE_PURPLE_SPEED)
        self._direction = random.randint(1,2) # 1 = right, 2 = left
        randomPosition = None
        if self._direction == 1:
            randomPosition = 0, random.randint(0, config.DISPLAY_HEIGHT)
        else:
            randomPosition = config.DISPLAY_WIDTH, random.randint(0, config.DISPLAY_HEIGHT)
        self.setPosition(randomPosition)

    def isOut(self):
        position = self.getPosition()
        if 0 >= position[0] >= config.DISPLAY_WIDTH:
             return True
        elif 0 >= position[1] >= config.DISPLAY_HEIGHT:
            return True
        else:
            return False

    def move(self, dodgeGame):
        if self.isOut():
            dodgeGame.killEnemie(self)
        else:
            if self._direction == 1:
                newPositionX = self._position[0] + (1 * self._speed)
                self.setPosition((newPositionX, self._position[1]))
            else:
                newPositionX = self._position[0] - (1 * self._speed)
                self.setPosition((newPositionX, self._position[1]))

    def getClass(self):
        return "PurpleEnemie"

class WhiteEnemie(Enemie):
    def __init__(self, position):
        super(WhiteEnemie, self).__init__(position,
                                           config.ENEMIE_WHITE_WIDTH,
                                           config.ENEMIE_WHITE_HEIGHT,
                                           config.ENEMIE_WHITE_IMAGE_small,
                                           config.ENEMIE_WHITE_SPEED)
        self._direction = random.randint(1,2) # 1 = down, 2 = up
        randomPosition = None
        if self._direction == 1:
            randomPosition = random.randint(0, config.DISPLAY_WIDTH-1), 0
        else:
            randomPosition = random.randint(0, config.DISPLAY_WIDTH-1), config.DISPLAY_HEIGHT-1
        self.setPosition(randomPosition)

    def isOut(self):
        position = self.getPosition()
        if 0 >= position[0] >= config.DISPLAY_WIDTH:
             return True
        elif 0 >= position[1] >= config.DISPLAY_HEIGHT:
            return True
        else:
            return False

    def move(self, dodgeGame):
        if self.isOut():
            dodgeGame.killEnemie(self)
        else:
            if self._direction == 1:
                newPositionY = self._position[1] + (1 * self._speed)
                self.setPosition((self._position[0], newPositionY))
            else:
                newPositionY = self._position[1] - (1 * self._speed)
                self.setPosition((self._position[0], newPositionY))

    def getClass(self):
        return "WhiteEnemie"
