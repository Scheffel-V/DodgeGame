import pygame
import config
import sys
import random
import os
import player as PLAYER
import game as GAME
import dodgegame as DODGEGAME
import enemie as ENEMIE
import wiimotemenu as WIIMOTEMENU
sys.path.insert(0, './pywiiuse')
import wiiuse.pygame_wiimote as pygame_wiimote

class Menu:
    def __init__(self):
        self._gameDisplay = None
        self._gameExit = False
        self._optionPointer = [10, 100]
        self._mainMenuImage0 = pygame.image.load(config.MENU_BACKGROUND_IMAGE_0)
        self._mainMenuImage1 = pygame.image.load(config.MENU_BACKGROUND_IMAGE_1)
        self._mainMenuImage2 = pygame.image.load(config.MENU_BACKGROUND_IMAGE_2)
        self._selectedOption = 0
        self._enemiesOnTheScreen = []
        for i in range(0, 4):
            self._enemiesOnTheScreen.append(self._generateEnemie())


    def _displayBackImage(self):
        if self._selectedOption == 0:
            mainMenuImage = self._mainMenuImage0
        elif self._selectedOption == 1:
            mainMenuImage = self._mainMenuImage1
        elif self._selectedOption == 2:
            mainMenuImage = self._mainMenuImage2
        else:
            print("You somehow selected an invalid option.")

        self._gameDisplay.blit(mainMenuImage, (0, 0))

    def _displayEnemies(self):
        for enemieAux in self._enemiesOnTheScreen:
            enemieAux.move(self)
            enemieAux.paint(self._gameDisplay)

    def _generateEnemie(self):
        enemieType = random.randint(0, 5)
        if enemieType == 0:
            return ENEMIE.ScreenEnemie((10, 10), config.ENEMIE_WHITE_IMAGE_small)
        elif enemieType == 1:
            return ENEMIE.ScreenEnemie((10, 10), config.ENEMIE_RED_IMAGE_small)
        elif enemieType == 2:
            return ENEMIE.ScreenEnemie((10, 10), config.ENEMIE_PURPLE_IMAGE_small)
        elif enemieType == 3:
            return ENEMIE.ScreenEnemie((10, 10), config.ENEMIE_BLUE_IMAGE_small)
        elif enemieType == 4:
            return ENEMIE.ScreenEnemie((10, 10), config.ENEMIE_YELLOW_IMAGE_small)
        else:
            return ENEMIE.ScreenEnemie((10, 10), config.ENEMIE_GREEN_IMAGE_small)

    def killEnemie(self, enemie):
        if self._enemiesOnTheScreen.__contains__(enemie):
            print("entrei")
            self._enemiesOnTheScreen.remove(enemie)
            self._enemiesOnTheScreen.append(self._generateEnemie())

    def _movePointerDown(self):
        self._optionPointer[1] += 50
        if self._optionPointer[1] > 200:
            self._optionPointer[1] = 100

        self._selectedOption = (self._selectedOption + 1) % 3


    def _movePointerUp(self):
        self._optionPointer[1] -= 50
        if self._optionPointer[1] < 100:
            self._optionPointer[1] = 200

        self._selectedOption -= 1
        if self._selectedOption < 0:
            self._selectedOption = 2

    def _startWiimoteMenu(self):
        wiimoteMenu = WIIMOTEMENU.WiimoteMenu(pygame)
        wiimoteMenu.start()

    def _handleMenuPress(self):
        if self._selectedOption == 0:
            self._startWiimoteMenu()

        elif self._selectedOption == 1:
            pass

        elif self._selectedOption == 2:
            self._gameExit = True

        else:
            raise ("You somehow selected an invalid option !")

    def _handleKeyPress(self, event):
        if event.key == pygame.K_DOWN:
            self._movePointerDown()

        if event.key == pygame.K_UP:
            self._movePointerUp()

        if event.key == pygame.K_SPACE:
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
        self._displayEnemies()

    def start(self):
        pygame.init()
        self._gameDisplay = pygame.display.set_mode((config.MENU_WIDTH, config.MENU_HEIGHT))
        pygame.display.set_caption("Main Menu")
        self._updateScreen()

        if os.name != 'nt': print('press 1&2')
        pygame_wiimote.init(1, 5) # look for 1, wait 5 seconds
        n = pygame_wiimote.get_count() # how many did we get?

        if n == 0:
            print('no wiimotes found')
            sys.exit(1)

        wm = pygame_wiimote.Wiimote(0) # access the wiimote object
        wm.enable_accels(1) # turn on acceleration reporting
        wm.enable_ir(1, vres=(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)) # turn on ir reporting

        old = [config.DISPLAY_HEIGHT/2] * 6
        maxA = 2.0

        while not self._gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._gameExit = True
                elif event.type == pygame.KEYDOWN:
                    self._handleKeyPress(event)
                elif event.type == pygame_wiimote.WIIMOTE_BUTTON_PRESS:
                    print(event.button, 'pressed on', event.id)
                    self._handleWiimotePress(event)
                elif event.type == pygame_wiimote.WIIMOTE_IR:
                    print("ENTREI YEY")
                    print(event.cursor[:2])
            self._updateScreen()
            pygame.display.update()
