from settings import *
from vec2D import Vec2d as Vec2D
import pygame
import balls
import math


class Cue:
    size = 3
    color = WHITE
    angel = 0

    def get_cue_pos(self, coords):
        start_pos = Vec2D(0, 0)
        end_pos = Vec2D(0, 0)
        r = 180
        r2 = 20
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angel -= 2
        if keys[pygame.K_RIGHT]:
            self.angel += 2
        if keys[pygame.K_UP]:
            self.angel -= 2
        if keys[pygame.K_DOWN]:
            self.angel += 2
        end_pos.x = coords.x + math.cos(math.radians(self.angel)) * r
        end_pos.y = coords.y + math.sin(math.radians(self.angel)) * r
        start_pos.x = coords.x + math.cos(math.radians(self.angel)) * r2
        start_pos.y = coords.y + math.sin(math.radians(self.angel)) * r2
        return (start_pos, end_pos)
