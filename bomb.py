import config
import rectangle
import pygame

class Bomb(rectangle.Rectangle):
    def __init__(self, position):
        super(Bomb, self).__init__(position, config.BOMB_WIDTH, config.BOMB_HEIGHT, config.BOMB_IMAGE)
        self._exploded = False
        self._catched = False
        self._timer = 2

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

    def paintRange(self, gameDisplay):
        _mouseCircleSurface = self._pygame.Surface(config.Config.MOUSE_CIRCLE_SURFACE)
        self._mouseCircleSurface.fill(config.Config.CK)
        self._mouseCircleSurface.set_colorkey(config.Config.CK)
        pygame.draw.circle(self._mouseCircleSurface, (254, 0, 0), self.getCenter(), self._range, self._range)
        self._mouseCircleSurface.set_alpha(150)
        gameDisplay.blit(self._mouseCircleSurface, (0, 0))