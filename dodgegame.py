# coding=utf-8
import pygame

import config
import time
import enemie
import map
import random


# Classe DodgeGame:
# A classe principal. É aqui que todas as interações do jogador com
# a partida são realizadas.
class DodgeGame:

    def __init__(self, player):
        self._playersList = []
        self._enemiesList = []
        self._loseGame = False
        self._FPS = False
        self._player = player
        self._playersList.append(player)
        self._timer = 0
        self._endTimer = 5
        self._enemieTimer = 1
        self._map = map.Map(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, "imagens/espaco2.jpg")

    def getPlayer(self):
        return self._player

    def getPlayers(self):
        return self._playersList

    def addEnemie(self, newEnemie):
        self._enemiesList.append(newEnemie)

    def spawnEnemie(self, enemie):
        self.addEnemie(enemie)
        self._enemieTimer = 1

    def delEnemie(self, enemie):
        if self._enemiesList.__contains__(enemie):
            self._enemiesList.remove(enemie)

    def getEnemies(self):
        return self._enemiesList

    def getEnemieToSpawn(self):
        randomNumber = random.randint(1, 4)
        randomPosition = random.randint(0, config.DISPLAY_WIDTH-1) , random.randint(0, config.DISPLAY_HEIGHT-1)

        if randomNumber == 1:
            return enemie.BlueEnemie(randomPosition)
        elif randomNumber == 2:
            return enemie.YellowEnemie(randomPosition)
        elif randomNumber == 3:
            return enemie.RedEnemie(randomPosition)
        else:
            return enemie.GreenEnemie(randomPosition)

    def paintAllStuff(self, gameDisplay, mousePosition):
        if not self._loseGame:
            self.paintMap(gameDisplay)
            self.paintName(gameDisplay)
            if self._enemieTimer == 0:
                self.spawnEnemie(self.getEnemieToSpawn())
                self.spawnEnemie(enemie.WhiteEnemie((0, 0)))
                self.spawnEnemie(enemie.PurpleEnemie((0, 0)))
            self.paintEnemies(gameDisplay)
            self.paintPlayers(gameDisplay, mousePosition)

    def paintMap(self, gameDisplay):
        self._map.paint(gameDisplay)

    def paintEnemies(self, gameDisplay):
        for enemiesAux in self.getEnemies():
            enemiesAux.move(self)
            enemiesAux.paint(gameDisplay)

    def paintPlayers(self, gameDisplay, mousePosition):
        for playersAux in self.getPlayers():
            playersAux.setPosition(mousePosition)
            playersAux.paint(gameDisplay)

    def paintMessage(self, gameDisplay, mousePosition, message):
        font = pygame.font.SysFont(None, 30, True, False)
        text = font.render(message, True, ((0, 0, 255)))
        gameDisplay.blit(text, (mousePosition[0]-50, mousePosition[1]-20))

    def paintLoseGameMessage(self, gameDisplay):
        font = pygame.font.SysFont(None, 100, True, False)
        text = font.render("YOU LOSE!", True, ((0, 0, 0)))
        gameDisplay.blit(text, (100, 100))
        text = font.render("WAVE:%d" % self._wave.getWaveNumber(), True, ((0, 0, 0)))
        gameDisplay.blit(text, (100, 150))

    def paintName(self, gameDisplay):
        font = pygame.font.SysFont(None, 30)
        text = font.render("%s" % self._player.getName(), True, (0, 0, 0))
        gameDisplay.blit(text, (495, 402))

    def decTimer(self):
        if not self._loseGame:
            self._timer -= 1
            self._enemieTimer -= 1
        else:
            self._endTimer -= 1
            self.paintLoseGameMessage(gameDisplay)
            if self._endTimer == 0:
                pygame.quit()
                menu = MENU.Menu()
                menu.start()

    def playerLose(self, gameDisplay):
        self._loseGame = True

    def getTimer(self):
        return self._timer
