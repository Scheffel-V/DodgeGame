import pygame
import config
import pygame
import random
import player as PLAYER
import game as GAME
import dodgegame as DODGEGAME


class Menu:
    def __init__(self):
        self._gameDisplay = None
        self._gameExit = False
        self._optionPointer = [10, 100]
        self._optionImage = pygame.image.load(config.MENU_POINTER)
        self._selectedOption = 0

    def _displayBackImage(self):
        mainMenuImage= pygame.image.load(config.MENU_BACKGROUND_IMAGE)
        self._gameDisplay.blit(mainMenuImage, (0, 0))

    def _displayText(self):
        myfont = pygame.font.Font(config.MAIN_MENU_FONT, 35)

        newGame = myfont.render("START", 1, (255,0,0))
        records = myfont.render("RECORDS", 1, (255,0,0))
        exit = myfont.render("EXIT", 1, (255,0,0))


        self._gameDisplay.blit(newGame, (65, 100))
        self._gameDisplay.blit(records, (65, 150))
        self._gameDisplay.blit(exit, (65, 200))

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

    def _startNewGame(self, playerName):
        game = GAME.Game()
        game.start()
        player = PLAYER.Player("Vinicius", (100, 100), 50, 50, config.PLAYER_ONE_IMAGE)
        dodgeGame = DODGEGAME.DodgeGame(player)

        while not game.getGameExit():
            mousePosition = game.getMousePosition()

            for event in game.getEvents():
                if event.type == pygame.QUIT:
                    game.setGameExit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if game.isFPSOn():
                            game.turnOffFPS()
                        else:
                            game.turnOnFPS()
                    if event.key == pygame.K_p:
                        if dodgeGame.isRunning():
                            if dodgeGame.isPaused():
                                dodgeGame.resumeGame()
                            else:
                                dodgeGame.pauseGame()
                elif event.type == pygame.USEREVENT + 1 and not dodgeGame.isPaused():
                    dodgeGame.decTimer()

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

    def _handleMenuPress(self):
        if self._selectedOption == 0:
            self._startNewGame("Vinicius")

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


    def _displaySelectedOption(self):
        self._gameDisplay.blit(self._optionImage, self._optionPointer)

    def _updateScreen(self):
        self._displayBackImage();
        self._displayText();
        self._displaySelectedOption();


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
