import pygame
import config
import sys
import random
import os
#sys.path.insert(0, './pywiiuse')
#import wiiuse.pygame_wiimote as pygame_wiimote
import abc

class Screen:
    def __init__(self, selectedOptionsNumber, pygame):
        self._gameDisplay = None
        self._gameExit = False
        self._mainImage = None
        self._selectedOptionsNumber = selectedOptionsNumber
        self._selectedOption = 0
        self._pygame = pygame

    def isGameExited(self):
        return self._gameExit

    def _incSelectedOption(self):
        self._selectedOption = (self._selectedOption + 1) % self._selectedOptionsNumber

    def _decSelectedOption(self):
        self._selectedOption -= 1
        if self._selectedOption < 0:
            self._selectedOption = self._selectedOptionsNumber - 1

    def _setTitle(self, title):
        self._pygame.display.set_caption(title)

    def _setDisplay(self, width, height):
        self._gameDisplay = self._pygame.display.set_mode((width, height))

    def _displayUpdate(self):
        self._pygame.display.update()

    def quit(self):
        self._pygame.quit()

    @abc.abstractmethod
    def _displayBackImage(self):
        pass

    @abc.abstractmethod
    def _changeBackImage(self):
        return

    @abc.abstractmethod
    def _updateScreen(self):
        return

    @abc.abstractmethod
    def _handleSelectedButtonPress(self):
        return

    @abc.abstractmethod
    def _handleKeyPress(self, event):
        return

    @abc.abstractmethod
    def _handleWiimotePress(self, event):
        return

    @abc.abstractmethod
    def _loopHandler(self):
        return

    @abc.abstractmethod
    def start(self):
        return
