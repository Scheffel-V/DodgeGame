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
    def __init__(self, pygame, menu, time):
        super().__init__(0, pygame)
        self._gameDisplay = None
        self._menu = menu
        self._gameTime = time
        self._mainImage = pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_0)

    def _updateScreen(self):
        #self._changeBackImage()
        self._displayBackImage()
        self.paintTime(self._gameDisplay)
        self._displayUpdate()

    def _saveRecord(self):
        pass

    def _showRecords(self):
        pass

    def _backToMenu(self):
        self._gameExit = True

    def _deleteLetter(self):
        pass

    def _handleKeyboardLetterInsertion(self, event):
        pass

    def _handleKeyPress(self, event):
        if event.key == self._pygame.K_ENTER:
            self._saveRecord()
            self._showRecords()

        if event.key == self._pygame.K_ESCAPE:
            self._backToMenu()

        if event.key == self._pygame.K_BACKSPACE:
            self._deleteLetter()

        else:
            self._handleKeyboardLetterInsertion(event)

    def _decLetter(self):
        pass

    def _incLetter(self):
        pass

    def _moveLetterPosition(self, direction):
        pass

    def _handleWiimoteLetterInsertion(self):
        pass

    def _handleWiimotePress(self, event):
        if event.button == 'Up':
            self._decLetter()

        elif event.button == 'Down':
            self._incLetter()

        elif event.button == 'Right':
            self._moveLetterPosition('Right')

        elif event.button == 'Left':
            self._moveLetterPosition('Left')

        elif event.button == 'A':
            self._handleWiimoteLetterInsertion()

        elif event.button == 'B':
            self._backToMenu()

        else:
            pass

    def paintTime(self, gameDisplay):
        font = self._pygame.font.SysFont(None, 50, True, False)
        text = font.render("TIME:%d" % self._gameTime, True, ((140, 160, 50)))
        gameDisplay.blit(text, (0, 0))

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
        self._setTitle("YOU WIN!")
        self._loopHandler()
