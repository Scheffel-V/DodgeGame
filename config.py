# coding=utf-8
# Classe Config:
#   Determina todas as propriedades do jogo.
#   É dessa classe que os valores numéricos que moldam o jogo
#   serão pegos. Basicamente, são os valores globais.

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CK = (255, 0, 0)
COLLIDE_COLOR = (255, 150, 0)
NOT_COLLIDE_COLOR = (0, 255, 0)
FPS = 100
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 1024
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
MOUSE_CIRCLE_SURFACE = (480, 480)

#BOMB
BOMB_IMAGE = "imagens/firetrap2.png"
BOMB_WIDTH = 32
BOMB_HEIGHT = 32

#SOUNDS
DEATH_SOUND = "sounds/death_sound.wav"
WIN_SOUND = "sounds/win_sound.wav"
EXPLOSION_SOUND = "sounds/explosion_sound.wav"
GAME_SONG = "sounds/game_song.wav"
MENU_SONG = "sounds/menu_song.wav"
DESPACITO = "sounds/despacito.wav"

#Map
MAP_BACKGROUND = "imagens/black.jpg"

#MOUSE
LEFT_BUTTON = 1
MIDDLE_BUTTON = 2
RIGHT_BUTTON = 3

#MENU
MENU_POINTER = "imagens/menu_pointer.png"
MENU_BACKGROUND_IMAGE_0 = "imagens/menu_main_0.png"
MENU_BACKGROUND_IMAGE_1 = "imagens/menu_main_1.png"
MENU_BACKGROUND_IMAGE_2 = "imagens/menu_main_2.png"
MAIN_MENU_FONT = "fonts/Colleged.ttf"
MENU_WIDTH = 460
MENU_HEIGHT = 620

#ENDGAME
ENDGAME_BACKGROUND_IMAGE_0 = "imagens/end game menu.png"
ENDGAME_BACKGROUND_IMAGE_1 = "imagens/end game menu_1.png"
ENDGAME_BACKGROUND_IMAGE_2 = "imagens/end game menu_2.png"
ENDGAME_BACKGROUND_IMAGE_3 = "imagens/end game menu_3.png"
ENDGAME_BACKGROUND_IMAGE_4 = "imagens/end game menu_4.png"
ENDGAME_BACKGROUND_IMAGE_5 = "imagens/end game menu_5.png"
ENDGAME_BACKGROUND_IMAGE_6 = "imagens/end game menu_6.png"
ENDGAME_BACKGROUND_IMAGE_7 = "imagens/end game menu_7.png"
ENDGAME_BACKGROUND_IMAGE_8 = "imagens/end game menu_8.png"
ENDGAME_BACKGROUND_IMAGE_9 = "imagens/end game menu_9.png"
ENDGAME_BACKGROUND_IMAGE_10 = "imagens/end game menu_10.png"
ENDGAME_WIDTH = 725
ENDGAME_HEIGHT = 725

#PLAYERS
PLAYER_ONE_IMAGE = "imagens/player-red.png"
PLAYER_TWO_IMAGE = "imagens/player-blue.png"
PLAYER_THREE_IMAGE = "imagens/player-green.png"
PLAYER_FOUR_IMAGE = "imagens/player-yellow.png"
PLAYER_IMAGE = []
PLAYER_IMAGE.append(PLAYER_ONE_IMAGE)
PLAYER_IMAGE.append(PLAYER_TWO_IMAGE)
PLAYER_IMAGE.append(PLAYER_THREE_IMAGE)
PLAYER_IMAGE.append(PLAYER_FOUR_IMAGE)

#ENEMIES
ENEMIE_BLUE_IMAGE_small = "imagens/blue.png"
ENEMIE_BLUE_WIDTH = 32
ENEMIE_BLUE_HEIGHT = 32
ENEMIE_BLUE_SPEED = 0.4

ENEMIE_RED_IMAGE_small = "imagens/red.png"
ENEMIE_RED_WIDTH = 32
ENEMIE_RED_HEIGHT = 32
ENEMIE_RED_SPEED = 1.2

ENEMIE_GREEN_IMAGE_small = "imagens/green.png"
ENEMIE_GREEN_WIDTH = 32
ENEMIE_GREEN_HEIGHT = 32
ENEMIE_GREEN_SPEED = 0.6

ENEMIE_YELLOW_IMAGE_small = "imagens/yellow.png"
ENEMIE_YELLOW_WIDTH = 32
ENEMIE_YELLOW_HEIGHT = 32
ENEMIE_YELLOW_SPEED = 0.8

ENEMIE_PURPLE_IMAGE_small = "imagens/purple.png"
ENEMIE_PURPLE_WIDTH = 32
ENEMIE_PURPLE_HEIGHT = 32
ENEMIE_PURPLE_SPEED = 1.0

ENEMIE_WHITE_IMAGE_small = "imagens/white.png"
ENEMIE_WHITE_WIDTH = 32
ENEMIE_WHITE_HEIGHT = 32
ENEMIE_WHITE_SPEED = 1.0

ENEMIE_SCREEN_WIDTH = 32
ENEMIE_SCREEN_HEIGHT = 32
ENEMIE_SCREEN_SPEED = 0.75
