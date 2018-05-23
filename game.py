# coding=utf-8
import pygame
import config

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

    def start(self):
        self._gameDisplay = self._pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        self._pygame.display.set_caption("Dodge Game")
        self._clock = self._pygame.time.Clock()
        self._pygame.time.set_timer(self._pygame.USEREVENT + 1, 1000)  # 1 second is 1000 milliseconds

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
