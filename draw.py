import pygame
from settings import SCREEN_SIZE, CUE_WIDTH


class Draw():
    def __init__(self):
        self.game_surface = pygame.Surface(SCREEN_SIZE)

    def draw_balls(self, ball):
        pygame.draw.circle(self.game_surface, ball.COLOR,
                           (int(ball.coords.x), int(ball.coords.y)),
                           ball.RADIUS)

    def cue_draw(self, cue, start_pos, end_pos):
        pygame.draw.line(self.game_surface, cue.color,
                         (int(start_pos.x), int(start_pos.y)), (int(end_pos.x),
                         int(end_pos.y)), CUE_WIDTH)
