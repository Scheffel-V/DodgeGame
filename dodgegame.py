# coding=utf-8
import pygame
#import wiiuse.pygame_wiimote as pygame_wiimote

import config
import time
import enemie
import map
import random
import bomb as BOMB
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
        self._endTimer = 4
        self._enemieTimer = 5
        self._difficultyTimer = 10
        self._bombTimer = 4
        self._gameIsRunning = True
        self._gameIsPaused = False
        self._gameTime = 0
        self._map = map.Map(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, config.MAP_BACKGROUND)
        self._pygame = game._pygame
        self._game = game
        self._sounds = []
        self._initializeSounds()
        self._bombsList = []
        self._explodedBombsList = []

    def _initializeSounds(self):
        self._sounds.append(self._pygame.mixer.Sound(config.GAME_SONG))
        self._sounds.append(self._pygame.mixer.Sound(config.WIN_SOUND))
        self._sounds.append(self._pygame.mixer.Sound(config.DEATH_SOUND))
        self._sounds.append(self._pygame.mixer.Sound(config.EXPLOSION_SOUND))
        self._sounds[0].set_volume(0.1)
        self._sounds[1].set_volume(0.5)
        self._sounds[2].set_volume(0.5)
        self._sounds[3].set_volume(0.5)

    def _increaseDifficulty(self):
        pass

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
        randomNumber = random.randint(1, 5)
        randomPosition = random.randint(0, config.DISPLAY_WIDTH-1) , random.randint(0, config.DISPLAY_HEIGHT-1)

        if randomNumber == 1:
            return enemie.BlueEnemie(randomPosition)
        elif randomNumber == 2:
            return enemie.YellowEnemie(randomPosition)
        elif randomNumber == 3:
            return enemie.RedEnemie(randomPosition)
        else:
            return enemie.GreenEnemie(randomPosition)

    def addBomb(self, newBomb):
        self._bombsList.append(newBomb)

    def _spawnBomb(self):
        randomNumber = random.randint(1, 3)
        if True:
            randomPosition = random.randint(0, config.DISPLAY_WIDTH - 1), random.randint(0, config.DISPLAY_HEIGHT - 1)
            bomb = BOMB.Bomb(randomPosition)
            self.addBomb(bomb)
        self._bombTimer = 4

    def explodeBomb(self, bomb):
        self._explodedBombsList.append(bomb)

    def killBomb(self, bomb):
        self._explodedBombsList.remove(bomb)

    def catchBomb(self, bomb):
        self._bombsList.remove(bomb)

    def singlePlayerExplodeBomb(self):
        self._playersList[0].explodeBomb(self)

    def playGameSong(self):
        self._sounds[0].play(-1)
        self._sounds[0].set_volume(0.3)

    def stopGameSong(self):
        self._sounds[0].stop()

    def _playWinSound(self):
        self._sounds[1].play()

    def _playDeathSound(self):
        self._sounds[2].play()

    def _playExplosionSound(self):
        self._sounds[3].play()

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

            if self._bombTimer <= 0:
                self._spawnBomb()

            if self._difficultyTimer <= 0:
                self._increaseDifficulty()

            self.paintEnemies(gameDisplay)
            self.paintPlayers(gameDisplay, playerPositionList)
            self.paintBombs(gameDisplay)
            self.paintTime(gameDisplay)

    def paintMap(self, gameDisplay):
        self._map.paint(gameDisplay)

    def paintEnemies(self, gameDisplay):
        for enemieAux in self.getEnemies():
            enemieAux.move(self)
            enemieAux.paint(gameDisplay)
            for bombAux in self._explodedBombsList:
                if bombAux.collide(enemieAux):
                    self.killEnemie(enemieAux)

    def paintPlayers(self, gameDisplay, playerPositionList):
        for playerAux in self.getAlivePlayers():
            for playerPositionAux in playerPositionList:
                if playerAux.getId() == playerPositionAux[0]:
                    playerAux.addNewLastPosition(playerPositionAux[1])
                    playerAux.paint(gameDisplay)
                    if playerAux.isColliding(self.getEnemies()):
                        if self.isTheLastPlayer():
                            self.stopGame()
                            self.paintWinGameMessage(gameDisplay)
                            self.stopGameSong()
                            self._playWinSound()
                            self._loseGame = True
                        else:
                            playerAux.kill(self)
                            self._playDeathSound()
                    if not playerAux.haveBomb():
                        for bombAux in self._bombsList:
                            if bombAux.collide(playerAux):
                                bombAux.catch()
                                self.catchBomb(bombAux)
                                playerAux.catchBomb(bombAux)

    def paintBombs(self, gameDisplay):
        for bombAux in self._bombsList:
            bombAux.paint(gameDisplay)

        for bombAux2 in self._explodedBombsList:
            bombAux2.paint(gameDisplay)

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
            self._difficultyTimer -= 1
            self._bombTimer -= 1
            for bombAux in self._explodedBombsList:
                bombAux.decTimer()
                if bombAux.isTimeUp():
                    self.killBomb(bombAux)
        else:
            self._endTimer -= 1
            if self._endTimer == 0:
                self._game.setGameExited()

    def playerLose(self, gameDisplay):
        self._loseGame = True

    def getTimer(self):
        return self._timer
