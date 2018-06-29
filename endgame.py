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
        super().__init__(10, pygame)
        self._gameDisplay = None
        self._menu = menu
        self._gameTime = time
        self._loadImages()
        self._word = {1: ' ', 2: ' ', 3: ' ', 4: ' ', 5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' ', 10: ' '}
        self._wordNumbers = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
        self._selectedLetter = None

    def _loadImages(self):
        self._image1 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_1)
        self._image2 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_2)
        self._image3 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_3)
        self._image4 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_4)
        self._image5 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_5)
        self._image6 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_6)
        self._image7 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_7)
        self._image8 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_8)
        self._image9 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_9)
        self._image10 =  self._pygame.image.load(config.ENDGAME_BACKGROUND_IMAGE_10)
        self._mainImage = self._image1
        self._backgroundImage = self._pygame.image.load(config.MAP_BACKGROUND)

    def _changeBackImage(self):
        if self._selectedOption == 0:
            self._mainImage = self._image1
        elif self._selectedOption == 1:
            self._mainImage = self._image2
        elif self._selectedOption == 2:
            self._mainImage = self._image3
        elif self._selectedOption == 3:
            self._mainImage = self._image4
        elif self._selectedOption == 4:
            self._mainImage = self._image5
        elif self._selectedOption == 5:
            self._mainImage = self._image6
        elif self._selectedOption == 6:
            self._mainImage = self._image7
        elif self._selectedOption == 7:
            self._mainImage = self._image8
        elif self._selectedOption == 8:
            self._mainImage = self._image9
        elif self._selectedOption == 9:
            self._mainImage = self._image10
        else:
            print("You somehow selected an invalid option.")

    def _updateScreen(self):
        self._changeBackImage()
        self._displayBackImage()
        self.paintTime(self._gameDisplay)
        self._paintWord(self._gameDisplay)
        self._displayUpdate()

    def _displayBackImage(self):
        self._gameDisplay.blit(self._backgroundImage, (0, 0))
        self._gameDisplay.blit(self._mainImage, ((config.DISPLAY_WIDTH / 2) - (config.ENDGAME_WIDTH / 2),
                                                 (config.DISPLAY_HEIGHT / 2) - (config.ENDGAME_HEIGHT / 2)))
    def _saveRecord(self):
        recordsFile = open("records.txt", "r+")
        records = []
        for i in range(1, 11):
            records.append(int((recordsFile.readline()).replace('\n', '')))
        recordsFile.close()

        for i in range(0, 10):
            if self._gameTime > records[i]:
                j = 9
                while j > i:
                    records[j] = records[j - 1]
                    j -= 1
                records[j] = self._gameTime
                break

        recordsFile = open("records.txt", "w")
        print(records)
        for i in range(0, 9):
            recordsFile.write((str(records[i])).__add__("\n"))
        recordsFile.write((str(records[9])))
        recordsFile.close()

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

    def _addLetter(self):
        self._word[self._selectedOption + 1] = self._getLetter(self._wordNumbers[self._selectedOption])
        print(self._word)

    def _getLetter(self, selectedLetter):
        return {
            1: 'a',
            2: 'b',
            3: 'c',
            4: 'd',
            5: 'e',
            6: 'f',
            7: 'g',
            8: 'h',
            9: 'i',
            10: 'j',
            11: 'k',
            12: 'l',
            13: 'm',
            14: 'n',
            15: 'o',
            16: 'p',
            17: 'q',
            18: 'r',
            19: 's',
            20: 't',
            21: 'u',
            22: 'v',
            23: 'w',
            24: 'x',
            25: 'y',
            26: 'z',
            None: ' '
        }[selectedLetter]

    def _decLetter(self):
        if self._wordNumbers[self._selectedOption] is None:
            self._wordNumbers[self._selectedOption] = 26
        else:
            self._wordNumbers[self._selectedOption] -= 1
            if self._wordNumbers[self._selectedOption] < 1:
                self._wordNumbers[self._selectedOption] = None
        self._addLetter()

    def _incLetter(self):
        if self._wordNumbers[self._selectedOption] is None:
            self._wordNumbers[self._selectedOption] = 1
        else:
            self._wordNumbers[self._selectedOption] += 1
            if self._wordNumbers[self._selectedOption] > 26:
                self._wordNumbers[self._selectedOption] = None
        self._addLetter()


    def _moveLetterPosition(self, direction):
        if direction is 'Right':
            self._incSelectedOption()
        elif direction is 'Left':
            self._decSelectedOption()

    def _handleWiimoteLetterInsertion(self):
        pass

    def _handleWiimotePress(self, event):
        if event.button == 'Up':
            self._incLetter()

        elif event.button == 'Down':
            self._decLetter()

        elif event.button == 'Right':
            self._moveLetterPosition('Right')

        elif event.button == 'Left':
            self._moveLetterPosition('Left')

        elif event.button == 'A':
            self._saveRecord()

        elif event.button == 'B':
            self._backToMenu()

        else:
            pass

    def paintTime(self, gameDisplay):
        font = self._pygame.font.SysFont(None, 50, True, False)
        text = font.render("TIME:%d" % self._gameTime, True, ((140, 160, 50)))
        gameDisplay.blit(text, (0, 0))

    def _paintWord(self, gameDisplay):
        font = self._pygame.font.SysFont(None, 50, True, False)
        for i in range (1, 11):
            text = font.render("%c" % self._word[i], True, ((254, 254, 254)))
            gameDisplay.blit(text, (((config.DISPLAY_WIDTH / 2) - (config.ENDGAME_WIDTH / 2) + 196) + (i - 1) * 36,
                                    ((config.DISPLAY_HEIGHT / 2) - (config.ENDGAME_HEIGHT /2) + 400)))

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
