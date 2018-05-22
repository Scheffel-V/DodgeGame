import pygame
import config
import random
import os

import player as PLAYER
import game as GAME
import dodgegame as DODGEGAME


class WiimoteMenu:
    def __init__(self):
        self._gameDisplay = None
        self._gameExit = False
        self._optionPointer = [10, 100]
        self._selectedOption = 0
        self._menuImage1 = pygame.image.load(config.WIIMOTE_MENU_BACKGROUND_IMAGE_1)
        self._menuImage2 = pygame.image.load(config.WIIMOTE_MENU_BACKGROUND_IMAGE_2)
        self._menuImage3 = pygame.image.load(config.WIIMOTE_MENU_BACKGROUND_IMAGE_3)
        self._menuImage4 = pygame.image.load(config.WIIMOTE_MENU_BACKGROUND_IMAGE_4)

    def _displayBackImage(self):
        if self._selectedOption == 0:
            menuImage = self._menuImage1
        elif self._selectedOption == 1:
            menuImage = self._menuImage2
        elif self._selectedOption == 2:
            menuImage = self._menuImage3
        elif self._selectedOption == 3:
            menuImage = self._menuImage4
        else:
            print("You somehow selected an invalid option.")

        self._gameDisplay.blit(menuImage, (0, 0))

    def _movePointerDown(self):
        self._selectedOption = (self._selectedOption + 1) % 4


    def _movePointerUp(self):
        self._selectedOption -= 1
        if self._selectedOption < 0:
            self._selectedOption = 3

    def _handleMenuPress(self):
        if self._selectedOption == 0:
            self._handleWiimoteMenu()


        elif self._selectedOption == 1:
            pass

        elif self._selectedOption == 2:
            pass

        elif self._selectedOption == 3:
            pass

        else:
            raise ("You somehow selected an invalid option !")

    def _handleKeyPress(self, event):
        if event.key == pygame.K_DOWN:
            self._movePointerDown()

        if event.key == pygame.K_UP:
            self._movePointerUp()

        if event.key == pygame.K_SPACE:
            self._handleMenuPress()

    def _updateScreen(self):
        self._displayBackImage()

    def _handleWiimoteMenu(self):
        if os.name != 'nt': print('press 1&2')
        pygame_wiimote.init(1, 5) # look for 1, wait 5 seconds
        n = pygame_wiimote.get_count() # how many did we get?

        if n == 0:
            print('no wiimotes found')
            sys.exit(1)

        wm = pygame_wiimote.Wiimote(0) # access the wiimote object
        wm.enable_accels(1) # turn on acceleration reporting
        wm.enable_ir(1, vres=size) # turn on ir reporting

        old = [h/2] * 6
        maxA = 2.0


    def start(self):
        pygame.init()
        self._gameDisplay = pygame.display.set_mode((config.MENU_WIDTH, config.MENU_HEIGHT))
        pygame.display.set_caption("Main Menu")
        self._updateScreen()

        while not self._gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._gameExit = True
                if event.type == pygame.KEYDOWN:
                    self._handleKeyPress(event)
            self._updateScreen()
            pygame.display.update()
