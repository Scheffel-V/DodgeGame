import config
import rectangle
import pygame

class Bomb(rectangle.Rectangle):
    def __init__(self, position, pygame):
        super(Bomb, self).__init__(position, config.BOMB_WIDTH, config.BOMB_HEIGHT, config.BOMB_IMAGE)
        self._exploded = False
        self._catched = False
        self._timer = 2
        self._range = 125
        self._pygame = pygame
        self._mouseCircleSurface = self._pygame.Surface(config.DISPLAY_SIZE)

    def decTimer(self):
        self._timer -= 1

    def isTimeUp(self):
        if self._timer <= 0:
            return True
        return False

    def explode(self, dodgeGame, position):
        self.setPosition(position)
        dodgeGame.explodeBomb(self)

    def isExploded(self):
        return self._exploded

    def catch(self):
        self._catched = True

    def isColliding(self, player):
        for playerAux in playersList:
            if self.collide(playerAux):
                return True
        return False

    def explosionCollide(self, enemie):
        circleX, circleY = self.getPosition()
        rectX, rectY = enemie.getPosition()
        circleDistanceX = abs(circleX - rectX);
        circleDistanceY = abs(circleY - rectY);

        if circleDistanceX > (enemie.getWidth() / 2 + self._range):
            return False
        if circleDistanceY > (enemie.getHeight() / 2 + self._range):
            return False
        if circleDistanceX <= (enemie.getWidth() / 2):
            return True
        if circleDistanceY <= (enemie.getHeight() / 2):
            return True

        cornerDistance_sq = ((circleDistanceX - enemie.getWidth() / 2) ** 2) + ((circleDistanceY - enemie.getHeight() / 2) ** 2)

        return cornerDistance_sq <= (self._range ** 2)

    def paintRange(self, gameDisplay):
        self._mouseCircleSurface.fill((255, 0, 0))
        self._mouseCircleSurface.set_colorkey((255, 0, 0))
        self._pygame.draw.circle(self._mouseCircleSurface, (254, 0, 0), self.getCenter(), self._range, self._range)
        self._mouseCircleSurface.set_alpha(150)
        gameDisplay.blit(self._mouseCircleSurface, (0, 0))
