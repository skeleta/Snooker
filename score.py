import pygame
from settings import *


class Score():
    pygame.font.init()

    def __init__(self):
        self.myfont = pygame.font.SysFont("monospace", 20, True)
        self.score_board = pygame.Surface((LEN_X, LEN_Y))

    def show_score(self, first_player, second_player, turn):
        self.score_board.fill(BACKGROUND_COLOR)
        first_player_name = self.myfont.render(first_player.name, 1, YELLOW)
        second_player_name = self.myfont.render(second_player.name, 1, YELLOW)
        first_player_score = self.myfont.render(str(first_player.points), 1,
                                                YELLOW)
        second_player_score = self.myfont.render(str(second_player.points), 1,
                                                 YELLOW)
        first_player_turn = self.myfont.render("-->", 1, BLACK)
        second_player_turn = self.myfont.render("<--", 1, BLACK)
        separator = self.myfont.render(":", 1, YELLOW)
        first_score_pos_x = POINTS_POS_ONE - len(str(first_player.points))\
            * CHARACTER_SIZE / 2
        second_points_pos_x = POINTS_POS_TWO - len(str(second_player.points))\
            * CHARACTER_SIZE / 2
        second_name_pos_x = SECOND_POS - len(second_player.name)\
            * CHARACTER_SIZE
        self.score_board.blit(first_player_name, (FIRST_POS, POS_Y))
        self.score_board.blit(separator, (SEPARETOR_POS_X, POS_Y))
        self.score_board.blit(first_player_score, (first_score_pos_x, POS_Y))
        self.score_board.blit(second_player_name, (second_name_pos_x, POS_Y))
        self.score_board.blit(second_player_score,
                              (second_points_pos_x, POS_Y))
        if turn == first_player:
            self.score_board.blit(first_player_turn, (IND_POS_ONE, POS_Y))
        else:
            self.score_board.blit(second_player_turn, (IND_POS_TWO, POS_Y))
