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
import records as RECORDS
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
        self._records = []
        self._recordsNames = []
        self._getRecords()
        self._recordPosition = -1
        self._showingRecords = False

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

    def _getWord(self):
        word = ""
        for i in range(1, 11):
            word = word + self._word[i]
        word = word + "\n"
        return word

    def _isTopScore(self):
        isTopScore = False
        for i in range(0, 10):
            if self._gameTime > self._records[i]:
                isTopScore = True
                self._recordPosition = i
                return isTopScore
        return isTopScore

    def _getRecords(self):
        recordsFile = open("records.txt", "r+")
        for i in range(1, 11):
            self._records.append(int((recordsFile.readline()).replace('\n', '')))
            self._recordsNames.append(recordsFile.readline())
        recordsFile.close()

    def _saveRecord(self):
        for i in range(0, 10):
            if self._gameTime > self._records[i]:
                j = 9
                while j > i:
                    self._records[j] = self._records[j - 1]
                    self._recordsNames[j] = self._recordsNames[j - 1]
                    j -= 1
                self._records[j] = self._gameTime
                self._recordsNames[j] = self._getWord()
                break

        recordsFile = open("records.txt", "w")
        print(self._records)
        print(self._recordsNames)
        for i in range(0, 9):
            recordsFile.write((str(self._records[i])).__add__("\n"))
            recordsFile.write(self._recordsNames[i])
        recordsFile.write((str(self._records[9])).__add__("\n"))
        recordsFile.write((self._recordsNames[9]).replace('\n', ''))
        recordsFile.close()

    def _showRecords(self):
        recordScreen = RECORDS.Records(self._pygame, self._menu, self._recordPosition)
        recordScreen.start()
        self._gameExit = True
        self._showingRecords = True

    def _backToMenu(self):
        self._gameExit = True

    def _deleteLetter(self):
        self._word[self._selectedOption + 1] = ' '
        self._moveLetterPosition('Left')

    def _handleKeyboardLetterInsertion(self, event):
        if event.key == self._pygame.K_a:
            self._word[self._selectedOption + 1] = 'a'
        elif event.key == self._pygame.K_b:
            self._word[self._selectedOption + 1] = 'b'
        elif event.key == self._pygame.K_c:
            self._word[self._selectedOption + 1] = 'c'
        elif event.key == self._pygame.K_d:
            self._word[self._selectedOption + 1] = 'd'
        elif event.key == self._pygame.K_e:
            self._word[self._selectedOption + 1] = 'e'
        elif event.key == self._pygame.K_f:
            self._word[self._selectedOption + 1] = 'f'
        elif event.key == self._pygame.K_g:
            self._word[self._selectedOption + 1] = 'g'
        elif event.key == self._pygame.K_h:
            self._word[self._selectedOption + 1] = 'h'
        elif event.key == self._pygame.K_i:
            self._word[self._selectedOption + 1] = 'i'
        elif event.key == self._pygame.K_j:
            self._word[self._selectedOption + 1] = 'j'
        elif event.key == self._pygame.K_k:
            self._word[self._selectedOption + 1] = 'k'
        elif event.key == self._pygame.K_l:
            self._word[self._selectedOption + 1] = 'l'
        elif event.key == self._pygame.K_m:
            self._word[self._selectedOption + 1] = 'm'
        elif event.key == self._pygame.K_n:
            self._word[self._selectedOption + 1] = 'n'
        elif event.key == self._pygame.K_o:
            self._word[self._selectedOption + 1] = 'o'
        elif event.key == self._pygame.K_p:
            self._word[self._selectedOption + 1] = 'p'
        elif event.key == self._pygame.K_q:
            self._word[self._selectedOption + 1] = 'q'
        elif event.key == self._pygame.K_r:
            self._word[self._selectedOption + 1] = 'r'
        elif event.key == self._pygame.K_s:
            self._word[self._selectedOption + 1] = 's'
        elif event.key == self._pygame.K_t:
            self._word[self._selectedOption + 1] = 't'
        elif event.key == self._pygame.K_u:
            self._word[self._selectedOption + 1] = 'u'
        elif event.key == self._pygame.K_v:
            self._word[self._selectedOption + 1] = 'v'
        elif event.key == self._pygame.K_w:
            self._word[self._selectedOption + 1] = 'w'
        elif event.key == self._pygame.K_x:
            self._word[self._selectedOption + 1] = 'x'
        elif event.key == self._pygame.K_y:
            self._word[self._selectedOption + 1] = 'y'
        elif event.key == self._pygame.K_z:
            self._word[self._selectedOption + 1] = 'z'
        elif event.key == self._pygame.K_SPACE:
            self._word[self._selectedOption + 1] = ' '
        else:
            pass
        self._moveLetterPosition('Right')

    def _handleKeyPress(self, event):
        if event.key == self._pygame.K_INSERT:
            self._saveRecord()
            self._showRecords()

        elif event.key == self._pygame.K_ESCAPE:
            self._backToMenu()

        elif event.key == self._pygame.K_BACKSPACE:
            self._deleteLetter()

        else:
            self._handleKeyboardLetterInsertion(event)

    def _addLetter(self):
        self._word[self._selectedOption + 1] = self._getLetter(self._wordNumbers[self._selectedOption])

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
            self._showRecords()

        elif event.button == 'B':
            self._backToMenu()

        else:
            pass

    def paintTime(self, gameDisplay):
        font = self._pygame.font.SysFont(None, 50, True, False)
        text = font.render("TIME:%d" % self._gameTime, True, (140, 160, 50))
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
                    self._handleWiimotePress(event)
            self._updateScreen()
        if not self._showingRecords:
            self._menu.restart()

    def start(self):
        if self._isTopScore():
            self._setDisplay(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
            self._setTitle("YOU WIN!")
            self._loopHandler()
        else:
            self._showRecords()
