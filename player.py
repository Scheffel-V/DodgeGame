import config
import rectangle
import pygame

# Classe Player:
# Classe que define a profile do jogador atual, assim como os
# atributos que ele tem da partida atual.
class Player(rectangle.Rectangle):
    def __init__(self, name, position, width, height, image):
        super(Player, self).__init__(position, width, height, image)
        self._name = name

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
