import pygame
import config
import sys
import random
import os
import screen as SCREEN
import player as PLAYER
import game as GAME
import dodgegame as DODGEGAME
import enemie as ENEMIE
import records as RECORDS
sys.path.insert(0, './pywiiuse')
import wiiuse.pygame_wiimote as pygame_wiimote

class Menu(SCREEN.Screen):
    def __init__(self, pygame):
        super(Menu, self).__init__(3, pygame)
        self._mainMenuImage0 = self._pygame.image.load(config.MENU_BACKGROUND_IMAGE_0)
        self._mainMenuImage1 = self._pygame.image.load(config.MENU_BACKGROUND_IMAGE_1)
        self._mainMenuImage2 = self._pygame.image.load(config.MENU_BACKGROUND_IMAGE_2)
        self._backgroundImage = self._pygame.image.load(config.MAP_BACKGROUND)
        self._mainImage = self._mainMenuImage0
        self._numberOfPlayers = 0
        self._enemiesOnTheScreen = []
        self._sound = None
        for i in range(0, 8):
            self._enemiesOnTheScreen.append(self._generateEnemie())


    def _initializeSound(self):
        self._sound = self._pygame.mixer.Sound(config.MENU_SONG)

    def _changeBackImage(self):
        if self._selectedOption == 0:
            self._mainImage = self._mainMenuImage0
        elif self._selectedOption == 1:
            self._mainImage = self._mainMenuImage1
        elif self._selectedOption == 2:
            self._mainImage = self._mainMenuImage2
        else:
            print("You somehow selected an invalid option.")

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
            self._enemiesOnTheScreen.remove(enemie)
            self._enemiesOnTheScreen.append(self._generateEnemie())

    def _startGame(self):
        self._sound.stop()
        game = GAME.Game(self._pygame, self)
        game.start(self._numberOfPlayers)

    def _showRecords(self):
        self._sound.stop()
        recordScreen = RECORDS.Records(self._pygame, self, -1)
        recordScreen.start()

    def _handleSelectedButtonPress(self):
        if self._selectedOption == 0:
            self._startGame()

        elif self._selectedOption == 1:
            self._showRecords()

        elif self._selectedOption == 2:
            self._gameExit = True

        else:
            raise ("You somehow selected an invalid option !")

    def _handleKeyPress(self, event):
        if event.key == self._pygame.K_DOWN:
            self._incSelectedOption()

        if event.key == self._pygame.K_UP:
            self._decSelectedOption()

        if event.key == self._pygame.K_SPACE:
            self._handleSelectedButtonPress()

    def _handleWiimotePress(self, event):
        if event.button == 'Up':
            self._decSelectedOption()

        elif event.button == 'Down':
            self._incSelectedOption()

        elif event.button == 'A':
            self._handleSelectedButtonPress()

        else:
            pass

    def _displayBackImage(self):
        self._gameDisplay.blit(self._backgroundImage, (0, 0))
        self._gameDisplay.blit(self._mainImage, ((config.DISPLAY_WIDTH / 2) - (config.MENU_WIDTH / 2),
                                                 (config.DISPLAY_HEIGHT / 2) - (config.MENU_HEIGHT / 2)))

    def _updateScreen(self):
        self._changeBackImage()
        self._displayBackImage()
        self._displayEnemies()
        self._displayUpdate()

    def _findWiimotes(self):
        if os.name != 'nt': print('press 1&2')
        pygame_wiimote.init(4, 10) # look for 1, wait 5 seconds
        n = pygame_wiimote.get_count() # how many did we get?

        if n == 0:
            print('no wiimotes found')
            sys.exit(1)

        self._numberOfPlayers = pygame_wiimote.get_count()
        for i in range(0, self._numberOfPlayers):
            print('Setting wiimote ', i + 1)
            wm = pygame_wiimote.Wiimote(i)
            wm.enable_accels(1)
            wm.enable_ir(1, vres=(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))

    def _playSong(self):
        self._sound.play(-1)
        self._sound.set_volume(0.3)

    def _stopSong(self):
        self._sound.stop()

    def _loopHandler(self):
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
                elif event.type == pygame_wiimote.WIIMOTE_IR:
                    if event.id not in idsList:
                        print('Wiimote ', event.id, ' is ok!')
                        idsList.append(event.id)
                elif event.type == 29:
                    if event.id not in idsList:
                        print('Wiimote ', event.id, ' is ok!')
                        idsList.append(event.id)
            self._updateScreen()
        self.quit()

    def restart(self):
        self._setDisplay(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self._setTitle("MENU")
        self._updateScreen()
        self._playSong()

    def start(self):
        self._pygame = pygame
        self._pygame.mixer.pre_init(44100, -16, 2, 4096)
        self._pygame.init()
        self._pygame.mixer.init()
        self._initializeSound()
        self._setDisplay(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self._setTitle("MENU")
        self._updateScreen()
        self._playSong()
        self._findWiimotes()
        self._loopHandler()
