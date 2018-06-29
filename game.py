# coding=utf-8
import pygame
import config
import random
import os
import sys
sys.path.insert(0, './pywiiuse')
import wiiuse.pygame_wiimote as pygame_wiimote
import screen as SCREEN
import player as PLAYER
import game as GAME
import endgame as ENDGAME
import dodgegame as DODGEGAME

class Game(SCREEN.Screen):
    def __init__(self, pygame, menu):
        super(Game, self).__init__(0, pygame)
        self._FPS = 0
        self._clock = 0
        self._playersList = []
        self._menu = menu

    def getPlayerList(self):
        return self._playersList

    def getClock(self):
        return self._clock

    def turnOnFPS(self):
        self._FPS = True

    def turnOffFPS(self):
        self._FPS = False

    def isFPSOn(self):
        return self._FPS

    def setGameExited(self):
        self._gameExit = True

    def paintAllStuff(self, gameDisplay, clock):
        if self.isFPSOn():
           self.paintFPS(gameDisplay, clock.get_fps())

    def paintFPS(self, gameDisplay, fps):
        font = self._pygame.font.SysFont(None, 25)
        text = font.render("FPS = %.2f" % fps, True, (140, 160, 50))
        gameDisplay.blit(text, (0, 30))

    def _loopHandler(self):
        dodgeGame = DODGEGAME.DodgeGame(self)
        playerPositionList = []
        while not self.isGameExited():
            playerPosition = None

            for event in self._pygame.event.get():
                if event.type == self._pygame.QUIT:
                    self.setGameExited()
                elif event.type == self._pygame.KEYDOWN:
                    if event.key == self._pygame.K_f:
                        if self.isFPSOn():
                            self.turnOffFPS()
                        else:
                            self.turnOnFPS()
                    if event.key == self._pygame.K_p:
                        if dodgeGame.isRunning():
                            if dodgeGame.isPaused():
                                dodgeGame.resumeGame()
                            else:
                                dodgeGame.pauseGame()
                elif event.type == self._pygame.USEREVENT + 1 and not dodgeGame.isPaused():
                    dodgeGame.decTimer()
                elif event.type == pygame_wiimote.WIIMOTE_IR:
                    mousePosition = event.cursor[:2]
                    playerPosition = (event.id, mousePosition)
                    playerPositionList.append(playerPosition)
                elif event.type == pygame_wiimote.WIIMOTE_BUTTON_PRESS:
                    print(event.button, 'pressed on', event.id)

            if dodgeGame.isRunning():
                if dodgeGame.isPaused():
                    dodgeGame.paintPauseGameMessage(self._gameDisplay)
                    self.getClock().tick()
                    self._displayUpdate()
                else:
                    dodgeGame.paintAllStuff(self._gameDisplay, playerPositionList)
                    playerPositionList = []
                    self.paintAllStuff(self._gameDisplay, self.getClock())
                    self.getClock().tick()
                    self._displayUpdate()
                    self.getClock().tick(config.FPS)      # Determina o FPS máximo
        endGame = ENDGAME.EndGame(self._pygame, self._menu, dodgeGame.getGameTime())
        endGame.start()

    def _startNewGame(self, numberOfPlayers):
        for i in range(0, numberOfPlayers):
            player = PLAYER.Player(i+1, (100, 100), 64, 64, i)
            self._playersList.append(player)

        self._loopHandler()

    def start(self, numberOfPlayers):
        self._setDisplay(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self._setTitle("DODGE GAME")
        self._clock = self._pygame.time.Clock()
        self._pygame.time.set_timer(self._pygame.USEREVENT + 1, 1000)  # 1 second is 1000 milliseconds
        self._startNewGame(numberOfPlayers)
