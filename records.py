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

class Records(SCREEN.Screen):
    def __init__(self, pygame, menu, recordPosition):
        super().__init__(0, pygame)
        self._gameDisplay = None
        self._menu = menu
        self._records = []
        self._recordsNames = []
        self._getRecords()
        self._loadImages()
        self._recordPosition = recordPosition

    def _loadImages(self):
        self._backgroundImage = self._pygame.image.load(config.MAP_BACKGROUND)

    def _changeBackImage(self):
        pass

    def _updateScreen(self):
        self._changeBackImage()
        self._displayBackImage()
        self._displayRecords()
        self._displayUpdate()

    def _displayBackImage(self):
        self._gameDisplay.blit(self._backgroundImage, (0, 0))

    def _displayRecords(self):
        self._getRecords()
        self._paintRecords()

    def _backToMenu(self):
        self._gameExit = True

    def _getRecords(self):
        recordsFile = open("records.txt", "r+")
        for i in range(1, 11):
            self._records.append(recordsFile.readline().replace('\n', ''))
            self._recordsNames.append(recordsFile.readline().replace('\n', ''))
        recordsFile.close()

    def _handleKeyPress(self, event):
        if event.key == self._pygame.K_ESCAPE:
            self._backToMenu()
        else:
            pass

    def _handleWiimotePress(self, event):
        if event.button == 'B':
            self._backToMenu()
        else:
            pass

    def _paintRecords(self):
        font = self._pygame.font.SysFont(None, 50, True, False)
        for i in range(0, 10):
            if i == self._recordPosition:
                position = font.render("%d" % (i + 1), True, (254, 0, 0))
                name = font.render("%s" % self._recordsNames[i], True, (254, 0, 0))
                score = font.render("%s" % self._records[i], True, (254, 0, 0))
            else:
                position = font.render("%d" % (i + 1), True, (254, 254, 254))
                name = font.render("%s" % self._recordsNames[i], True, (254, 254, 254))
                score = font.render("%s" % self._records[i], True, (254, 254, 254))

            self._gameDisplay.blit(position, (0 + (config.DISPLAY_WIDTH / 2) - 150,
                                             (config.DISPLAY_HEIGHT / 2) - 225 + i * 50))
            self._gameDisplay.blit(name, (75 + (config.DISPLAY_WIDTH / 2) - 150,
                                             (config.DISPLAY_HEIGHT / 2) - 225 + i * 50))
            self._gameDisplay.blit(score, (300 + (config.DISPLAY_WIDTH / 2) - 150,
                                             (config.DISPLAY_HEIGHT / 2) - 225 + i * 50))

    def _loopHandler(self):
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
        self._menu.restart()

    def start(self):
        self._setDisplay(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self._setTitle("RECORDS")
        self._loopHandler()
