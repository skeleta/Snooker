from settings import CUE_DEFAULT_R, BROWN
from vec2D import Vec2d as Vec2D
import pygame
import math


class Cue:
    def __init__(self):
        self.length = 160
        self.color = BROWN
        self.angle = 0
        self.r = CUE_DEFAULT_R


    def get_cue_pos(self, coords):
        start_pos = Vec2D(0, 0)
        end_pos = Vec2D(0, 0)
        r2 = self.r - self.length
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= 2
        if keys[pygame.K_RIGHT]:
            self.angle += 2
        if keys[pygame.K_UP]:
            self.r -= 1
        if self.r < CUE_DEFAULT_R:
            self.r = CUE_DEFAULT_R
        if keys[pygame.K_DOWN]:
            self.r += 1
        if self.r > CUE_DEFAULT_R + CUE_DEFAULT_R / 2:
            self.r = CUE_DEFAULT_R + CUE_DEFAULT_R / 2
        end_pos.x = coords.x + math.cos(math.radians(self.angle)) * self.r
        end_pos.y = coords.y + math.sin(math.radians(self.angle)) * self.r
        start_pos.x = coords.x + math.cos(math.radians(self.angle)) * r2
        start_pos.y = coords.y + math.sin(math.radians(self.angle)) * r2
        return (start_pos, end_pos)
