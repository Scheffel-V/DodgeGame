import config
import rectangle
import pygame

# Classe Player:
# Classe que define a profile do jogador atual, assim como os
# atributos que ele tem da partida atual.
class Player(rectangle.Rectangle):
    def __init__(self, id, position, width, height, image):
        super(Player, self).__init__(position, width, height, image)
        self._isAlive = True
        self._id = id

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
