# coding=utf-8
import pygame
import config
import random
import os
import sys
sys.path.insert(0, './pywiiuse')
import wiiuse.pygame_wiimote as pygame_wiimote
import player as PLAYER
import game as GAME
import dodgegame as DODGEGAME

# Classe Game:
# Classe utilizada assim que o jogo é aberto.
# É a interface que permeia o jogo desde o menu,
# durante a partida, até a hora que o jogador clica no exit.
class Game:
    def __init__(self, pygame):
        self._gameExit = False
        self._FPS = 0
        self._gameDisplay = 0
        self._clock = 0
        self._pygame = pygame
        self._playersList = []

    def setGameExit(self):
        self._gameExit = True

    def getGameExit(self):
        return self._gameExit

    def setGameDisplay(self, gameDisplay):
        self._gameDisplay = gameDisplay

    def getGameDisplay(self):
        return self._gameDisplay

    def setClock(self, clock):
        self._clock = clock

    def getClock(self):
        return self._clock

    def turnOnFPS(self):
        self._FPS = True

    def turnOffFPS(self):
        self._FPS = False

    def isFPSOn(self):
        return self._FPS

    def update(self):
        self._pygame.display.update()

    def quit(self):
        self._pygame.quit()

    def getMousePosition(self):
        return self._pygame.mouse.get_pos()

    def paintAllStuff(self, gameDisplay, clock):
        if self.isFPSOn():
           self.paintFPS(gameDisplay, clock.get_fps())

    def paintFPS(self, gameDisplay, fps):
        font = self._pygame.font.SysFont(None, 25)
        text = font.render("FPS = %.2f" % fps, True, (0,0,0))
        gameDisplay.blit(text, (0, 0))

    def _startNewGame(self, numberOfPlayers):
        for i in range(0, numberOfPlayers):
            player = PLAYER.Player(i+1, (100, 100), 64, 64, config.PLAYER_ONE_IMAGE)
            self._playersList.append(player)

        dodgeGame = DODGEGAME.DodgeGame(self._playersList)

        while not self.getGameExit():
            playerPosition = None

            for event in self._pygame.event.get():
                if event.type == self._pygame.QUIT:
                    self.setGameExit()
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
                elif event.type == pygame_wiimote.WIIMOTE_BUTTON_PRESS:
                    print(event.button, 'pressed on', event.id)

            if dodgeGame.isRunning():
                if dodgeGame.isPaused():
                    dodgeGame.paintPauseGameMessage(self.getGameDisplay())
                    self.getClock().tick()
                    self.update()
                else:
                    dodgeGame.paintAllStuff(self.getGameDisplay(), playerPosition)
                    self.paintAllStuff(self.getGameDisplay(), self.getClock())
                    self.getClock().tick()
                    self.update()
                    self.getClock().tick(config.FPS)      # Determina o FPS máximo
        self.quit()

    def start(self, numberOfPlayers):
        self._gameDisplay = self._pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        self._pygame.display.set_caption("Dodge Game")
        self._clock = self._pygame.time.Clock()
        self._pygame.time.set_timer(self._pygame.USEREVENT + 1, 1000)  # 1 second is 1000 milliseconds
        self._startNewGame(numberOfPlayers)
