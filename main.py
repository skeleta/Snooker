import pygame
from game import Game
from score import Score
from settings import *


def main():
    pygame.init()
    the_game = Game(SCREEN_SIZE)
    running = True

    while running:
        the_game.white_ball_grab()
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                running = False
        the_game.game_surface.fill(BACKGROUND_COLOR)
        the_game.game_surface.blit(the_game.table, TABLE_POS)
        the_game.game_handler()
        the_game.draw_balls()
        the_game.screen.blit(the_game.game_surface, (0, 0))
        the_game.screen.blit(Score.score_board, (408, 530))
        pygame.display.flip()
        the_game.clock.tick(100)
    pygame.quit()


if __name__ == '__main__':
    main()
    print("Game closed")
