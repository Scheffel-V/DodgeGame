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


class WiimoteMenu:
    def __init__(self, pygame):
        self._gameDisplay = None
        self._gameExit = False
        self._pygame = pygame
        self._optionPointer = [10, 100]
        self._selectedOption = 0
        self._menuImage1 = self._pygame.image.load(config.WIIMOTE_MENU_BACKGROUND_IMAGE_1)
        self._menuImage2 = self._pygame.image.load(config.WIIMOTE_MENU_BACKGROUND_IMAGE_2)
        self._menuImage3 = self._pygame.image.load(config.WIIMOTE_MENU_BACKGROUND_IMAGE_3)
        self._menuImage4 = self._pygame.image.load(config.WIIMOTE_MENU_BACKGROUND_IMAGE_4)

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
            self._startNewGame(1)


        elif self._selectedOption == 1:
            pass

        elif self._selectedOption == 2:
            pass

        elif self._selectedOption == 3:
            pass

        else:
            raise ("You somehow selected an invalid option !")

    def _handleKeyPress(self, event):
        if event.key == self._pygame.K_DOWN:
            self._movePointerDown()

        if event.key == self._pygame.K_UP:
            self._movePointerUp()

        if event.key == self._pygame.K_SPACE:
            self._handleMenuPress()

    def _handleWiimotePress(self, event):
        if event.button == 'Up':
            self._movePointerUp()

        elif event.button == 'Down':
            self._movePointerDown()

        elif event.button == 'A':
            self._handleMenuPress()

        else:
            pass

    def _updateScreen(self):
        self._displayBackImage()

    def _startNewGame(self, numberOfPlayers):
        game = GAME.Game(self._pygame)
        game.start()
        player = PLAYER.Player("Vinicius", (100, 100), 50, 50, config.PLAYER_ONE_IMAGE)
        dodgeGame = DODGEGAME.DodgeGame(player)

        while not game.getGameExit():
            #mousePosition = game.getMousePosition()
            mousePosition = None

            for event in self._pygame.event.get():
                if event.type == self._pygame.QUIT:
                    print(event)
                    print(event.type)
                    game.setGameExit()
                elif event.type == self._pygame.KEYDOWN:
                    print(event)
                    print(event.type)
                    if event.key == self._pygame.K_f:
                        if game.isFPSOn():
                            game.turnOffFPS()
                        else:
                            game.turnOnFPS()
                    if event.key == self._pygame.K_p:
                        if dodgeGame.isRunning():
                            if dodgeGame.isPaused():
                                dodgeGame.resumeGame()
                            else:
                                dodgeGame.pauseGame()
                elif event.type == self._pygame.USEREVENT + 1 and not dodgeGame.isPaused():
                    print(event)
                    print(event.type)
                    dodgeGame.decTimer()
                elif event.type == pygame_wiimote.WIIMOTE_IR:
                    print("ENTREI YEY")
                    mousePosition = event.cursor[:2]
                    print(mousePosition)

            if dodgeGame.isRunning():
                if dodgeGame.isPaused():
                    dodgeGame.paintPauseGameMessage(game.getGameDisplay())
                    game.getClock().tick()
                    game.update()
                else:
                    dodgeGame.paintAllStuff(game.getGameDisplay(), mousePosition)
                    game.paintAllStuff(game.getGameDisplay(), game.getClock())
                    game.getClock().tick()
                    game.update()
                    game.getClock().tick(config.FPS)      # Determina o FPS máximo
        game.quit()
        quit()

    def start(self):
        self._gameDisplay = self._pygame.display.set_mode((config.MENU_WIDTH, config.MENU_HEIGHT))
        self._pygame.display.set_caption("Number of Players")
        self._updateScreen()

        while not self._gameExit:
            for event in self._pygame.event.get():
                if event.type == self._pygame.QUIT:
                    self._gameExit = True
                elif event.type == self._pygame.KEYDOWN:
                    self._handleKeyPress(event)
                elif event.type == pygame_wiimote.WIIMOTE_BUTTON_PRESS:
                    print(event.type)
                    print(event)
                    print(event.button, 'pressed on', event.id)
                    self._handleWiimotePress(event)
            self._updateScreen()
            self._pygame.display.update()
