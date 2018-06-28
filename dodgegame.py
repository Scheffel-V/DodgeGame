# coding=utf-8
import pygame
#import wiiuse.pygame_wiimote as pygame_wiimote

import config
import time
import enemie
import map
import random
import game


# Classe DodgeGame:
# A classe principal. É aqui que todas as interações do jogador com
# a partida são realizadas.
class DodgeGame:

    def __init__(self, game):
        self._alivePlayersList = game.getPlayerList()
        self._enemiesList = []
        self._loseGame = False
        self._FPS = False
        self._playersList = game.getPlayerList()
        self._timer = 0
        self._endTimer = 5
        self._enemieTimer = 5
        self._gameIsRunning = True
        self._gameIsPaused = False
        self._gameTime = 0
        self._map = map.Map(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, config.MAP_BACKGROUND)
        self._pygame = game._pygame
        self._game = game

    def getGameTime(self):
        return self._gameTime

    def isRunning(self):
        return self._gameIsRunning

    def stopGame(self):
        self._gameIsRunning = False

    def isPaused(self):
        return self._gameIsPaused

    def pauseGame(self):
        self._gameIsPaused = True

    def resumeGame(self):
        self._gameIsPaused = False

    def getPlayers(self):
        return self._playersList

    def getAlivePlayers(self):
        return self._alivePlayersList

    def isTheLastPlayer(self):
        if len(self._alivePlayersList) == 1:
            return True
        else:
            return False

    def killPlayer(self, player):
        if self._alivePlayersList.__contains__(player):
            self._alivePlayersList.remove(player)

    def addEnemie(self, newEnemie):
        self._enemiesList.append(newEnemie)

    def spawnEnemie(self, enemie):
        self.addEnemie(enemie)
        self._enemieTimer = 2

    def killEnemie(self, enemie):
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

    def paintAllStuff(self, gameDisplay, playerPositionList):
        if not self._loseGame:
            self.paintMap(gameDisplay)
            if self._enemieTimer <= 0:
                self.spawnEnemie(self.getEnemieToSpawn())
                randomNumber = random.randint(1, 2)
                if randomNumber == 1:
                    self.spawnEnemie(enemie.WhiteEnemie((0, 0)))
                else:
                    self.spawnEnemie(enemie.PurpleEnemie((0, 0)))
            self.paintEnemies(gameDisplay)
            self.paintPlayers(gameDisplay, playerPositionList)
            self.paintTime(gameDisplay)

    def paintMap(self, gameDisplay):
        self._map.paint(gameDisplay)

    def paintEnemies(self, gameDisplay):
        for enemiesAux in self.getEnemies():
            enemiesAux.move(self)
            enemiesAux.paint(gameDisplay)

    def paintPlayers(self, gameDisplay, playerPositionList):
        print(len(playerPositionList))
        for playerAux in self.getAlivePlayers():
            for playerPositionAux in playerPositionList:
                if playerAux.getId() == playerPositionAux[0]:
                    playerAux.addNewLastPosition(playerPositionAux[1])
                    playerAux.paint(gameDisplay)
                    if playerAux.isColliding(self.getEnemies()):
                        if self.isTheLastPlayer():
                            self.stopGame()
                            self.paintWinGameMessage(gameDisplay)
                            self._loseGame = True
                        else:
                            playerAux.kill(self)

    def paintMessage(self, gameDisplay, mousePosition, message):
        font = self._pygame.font.SysFont(None, 30, True, False)
        text = font.render(message, True, ((0, 0, 255)))
        gameDisplay.blit(text, (mousePosition[0]-50, mousePosition[1]-20))

    def paintWinGameMessage(self, gameDisplay):
        font = self._pygame.font.SysFont(None, 100, True, False)
        text = font.render("YOU WIN!", True, ((254, 254, 254)))
        gameDisplay.blit(text, (config.DISPLAY_WIDTH / 2 - text.get_rect().width / 2, config.DISPLAY_HEIGHT / 2 - text.get_rect().height / 2))

    def paintPauseGameMessage(self, gameDisplay):
        font = self._pygame.font.SysFont(None, 100, True, False)
        text = font.render("GAME IS PAUSED", True, ((254, 254, 254)))
        gameDisplay.blit(text, (config.DISPLAY_WIDTH / 2 - text.get_rect().width / 2, config.DISPLAY_HEIGHT / 2 - text.get_rect().height / 2))

    def paintTime(self, gameDisplay):
        font = self._pygame.font.SysFont(None, 50, True, False)
        text = font.render("TIME:%d" % self._gameTime, True, ((140, 160, 50)))
        gameDisplay.blit(text, (0, 0))

    def paintName(self, gameDisplay):
        font = self._pygame.font.SysFont(None, 30)
        text = font.render("%s" % "MESTRE", True, (0, 0, 0))
        gameDisplay.blit(text, (495, 402))

    def decTimer(self):
        if self.isRunning():
            self._gameTime += 1
        if not self._loseGame:
            self._timer -= 1
            self._enemieTimer -= 1
        else:
            self._endTimer -= 1
            if self._endTimer == 0:
                self._game.setGameExited()

    def playerLose(self, gameDisplay):
        self._loseGame = True

    def getTimer(self):
        return self._timer
