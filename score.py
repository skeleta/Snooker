import pygame
from settings import *


class Score():
    pygame.font.init()

    def __init__(self):
        self.myfont = pygame.font.SysFont("monospace", 20, True)
        self.score_board = pygame.Surface((400, 50))

    def show_score(self, first_player, second_player, turn):
        self.score_board.fill(BACKGROUND_COLOR)
        first_player_name = self.myfont.render(first_player.name, 1,
                                               (255, 255, 0))
        second_player_name = self.myfont.render(second_player.name, 1,
                                                (255, 255, 0))
        first_player_score = self.myfont.render(str(first_player.points), 1,
                                                (255, 255, 0))
        second_player_score = self.myfont.render(str(second_player.points), 1,
                                                 (255, 255, 0))
        first_player_turn = self.myfont.render("-->", 1, (255, 255, 0))
        second_player_turn = self.myfont.render("<--", 1, (255, 255, 0))
        separator = self.myfont.render(":", 1, (255, 255, 0))
        self.score_board.blit(first_player_name, (0, 10))
        self.score_board.blit(first_player_score, (100, 10))
        self.score_board.blit(second_player_score, (150, 10))
        self.score_board.blit(second_player_name, (230, 10))
        self.score_board.blit(separator, (137, 10))
        if turn == first_player:
            self.score_board.blit(first_player_turn, (65, 10))
        else:
            self.score_board.blit(second_player_turn, (185, 10))
