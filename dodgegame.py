# coding=utf-8
import pygame
#import wiiuse.pygame_wiimote as pygame_wiimote

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
        self._alivePlayersList = []
        self._enemiesList = []
        self._loseGame = False
        self._FPS = False
        self._playersList.append(player)
        self._alivePlayersList.append(player)
        self._timer = 0
        self._endTimer = 5
        self._enemieTimer = 1000
        self._gameIsRunning = True
        self._gameIsPaused = False
        self._gameTime = 0
        self._map = map.Map(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, "imagens/espaco2.jpg")

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
        self._enemieTimer = 1

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

    def paintAllStuff(self, gameDisplay, mousePosition):
        if not self._loseGame:
            self.paintMap(gameDisplay)
            if self._enemieTimer == 0:
                self.spawnEnemie(self.getEnemieToSpawn())
                self.spawnEnemie(enemie.WhiteEnemie((0, 0)))
                self.spawnEnemie(enemie.PurpleEnemie((0, 0)))
            self.paintEnemies(gameDisplay)
            if mousePosition is not None:
                self.paintPlayers(gameDisplay, mousePosition)
            self.paintTime(gameDisplay)

    def paintMap(self, gameDisplay):
        self._map.paint(gameDisplay)

    def paintEnemies(self, gameDisplay):
        for enemiesAux in self.getEnemies():
            enemiesAux.move(self)
            enemiesAux.paint(gameDisplay)

    def paintPlayers(self, gameDisplay, mousePosition):
        for playerAux in self.getAlivePlayers():
            playerAux.setPosition(mousePosition)
            playerAux.paint(gameDisplay)
            if playerAux.isColliding(self.getEnemies()):
                if self.isTheLastPlayer():
                    self.stopGame()
                    self.paintWinGameMessage(gameDisplay)
                else:
                    playerAux.kill(self)

    def paintMessage(self, gameDisplay, mousePosition, message):
        font = pygame.font.SysFont(None, 30, True, False)
        text = font.render(message, True, ((0, 0, 255)))
        gameDisplay.blit(text, (mousePosition[0]-50, mousePosition[1]-20))

    def paintWinGameMessage(self, gameDisplay):
        font = pygame.font.SysFont(None, 100, True, False)
        text = font.render("YOU WIN!", True, ((0, 0, 0)))
        gameDisplay.blit(text, (config.DISPLAY_WIDTH / 2 - text.get_rect().width / 2, config.DISPLAY_HEIGHT / 2 - text.get_rect().height / 2))

    def paintPauseGameMessage(self, gameDisplay):
        font = pygame.font.SysFont(None, 100, True, False)
        text = font.render("GAME IS PAUSED", True, ((0, 0, 0)))
        gameDisplay.blit(text, (config.DISPLAY_WIDTH / 2 - text.get_rect().width / 2, config.DISPLAY_HEIGHT / 2 - text.get_rect().height / 2))

    def paintTime(self, gameDisplay):
        font = pygame.font.SysFont(None, 50, True, False)
        text = font.render("TIME:%d" % self._gameTime, True, ((140, 160, 50)))
        gameDisplay.blit(text, (0, 0))

    def paintName(self, gameDisplay):
        font = pygame.font.SysFont(None, 30)
        text = font.render("%s" % "MESTRE", True, (0, 0, 0))
        gameDisplay.blit(text, (495, 402))

    def decTimer(self):
        self._gameTime += 1
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
