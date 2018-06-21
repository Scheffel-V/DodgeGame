import pygame
import config
import sys
import random
import os
import player as PLAYER
import game as GAME
import dodgegame as DODGEGAME
import enemie as ENEMIE
import screen as SCREEN
sys.path.insert(0, './pywiiuse')
import wiiuse.pygame_wiimote as pygame_wiimote

class EndGame(SCREEN.Screen):
    def __init__(self, pygame):
        super().__init__(0, pygame)
        self._gameDisplay = None
        self._pygame = pygame
        self._mainImage = pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_0)

    def _updateScreen():
        self._changeBackImage()
        self._displayBackImage()
        self._displayUpdate()

    def _loopHandler():
        idsList = []
        while not self.isGameExited():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._gameExit = True
                elif event.type == pygame.KEYDOWN:
                    self._handleKeyPress(event)
                elif event.type == pygame_wiimote.WIIMOTE_BUTTON_PRESS:
                    print(event.button, 'pressed on', event.id)
                    self._handleWiimotePress(event)
            self._updateScreen()

    def start(self):
        self._setDisplay(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self._setTitle("YOU WIN!")
        self._clock = self._pygame.time.Clock()
        self._pygame.time.set_timer(self._pygame.USEREVENT + 1, 1000)  # 1 second is 1000 milliseconds
        self._loopHandler()
