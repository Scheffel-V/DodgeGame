# coding=utf-8
import pygame
import config
import dodgegame
import player
import game

game = game.Game()
game.start()
player = player.Player("Vinicius", (100, 100), 50, 50, config.PLAYER_ONE_IMAGE)
dodgeGame = dodgegame.DodgeGame(player)

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

        elif event.type == pygame.USEREVENT + 1:
             dodgeGame.decTimer()

    dodgeGame.paintAllStuff(game.getGameDisplay(), mousePosition)
    game.paintAllStuff(game.getGameDisplay(), game.getClock())
    game.getClock().tick()
    game.update()
    game.getClock().tick(config.FPS)      # Determina o FPS máximo

game.quit()
quit()
