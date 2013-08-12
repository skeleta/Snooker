import pygame
import math
from settings import *
from vec2D import Vec2d as Vec2D


class Ball():
    RADIUS = 8
    potted = []

    def __init__(self, coords, **kwds):
        self.coords = Vec2D(coords)
        self.pos = Vec2D(coords)
        # self.points = points
        # self.COLOR = COLOR
        self.velocity = Vec2D(0, 0)
        self.vizibility = True
        self.is_potted = False

    def move(self, pockets):
        check = Vec2D(self.velocity)
        self.velocity -= Vec2D.normalized(self.velocity) * FRICTION * TIMER
        self.coords += self.velocity * TIMER
        if check.x * self.velocity.x < 0:
            self.velocity = Vec2D(0, 0)
        if int(self.coords.x) not in range(139, 534) and\
                int(self.coords.x) not in range(564, 960)\
                and int(self.coords.y) not in range(90, 484):

            """Ако някоя от топките е в обсега на някой от джобовете
            влизаме в този if и почваме да следим за сблъсък със стената на
            някой от джобовете или за попадение в джоба"""

            for pocket in pockets:
                self.pocket_walls_collision(pockets[pocket][1], pockets[pocket][2])
                self.pocket_walls_collision(pockets[pocket][3], pockets[pocket][4])
                if (self.coords - pockets[pocket][0]).length <= POCKET_R:
                    # if self not in Ball.potted:
                    #     Ball.potted.append(self)
                    self.vizibility = False
                    self.coords = Vec2D(1000, 1000) + self.pos
                    self.velocity = Vec2D(0, 0)
                    self.is_potted = True
        else:
            if self.coords.x < LEFT_BORDER or self.coords.x > RIGHT_BORDER:
                if self.coords.x < LEFT_BORDER:
                    self.coords.x = LEFT_BORDER
                else:
                    self.coords.x = RIGHT_BORDER
                self.velocity.x = -self.velocity.x
            elif self.coords.y < UP_BORDER or self.coords.y > DOWN_BORDER:
                if self.coords.y < UP_BORDER:
                    self.coords.y = UP_BORDER
                else:
                    self.coords.y = DOWN_BORDER
                self.velocity.y = -self.velocity.y

    def pocket_walls_collision(self, start_point, end_point):
        incoming_vec = self.coords - start_point
        pocket_wall_vec = end_point - start_point
        projected = Vec2D.projection(incoming_vec, pocket_wall_vec)
        distance = Vec2D.get_distance(incoming_vec, projected)
        if 0 <= math.fabs(projected.x) <=\
                math.fabs(end_point.x - start_point.x) and\
                0 <= math.fabs(projected.y) <=\
                math.fabs(end_point.y - start_point.y) and\
                distance < self.RADIUS:
            self.coords = Vec2D.normalized(incoming_vec - projected) *\
                          self.RADIUS + start_point + projected
            self.velocity = 2 * (self.velocity.dot(pocket_wall_vec) /\
                            pocket_wall_vec.dot(pocket_wall_vec)) *\
                            pocket_wall_vec - self.velocity


class ColorBall(Ball):
    def __init__(self, COLOR, points, **kwds):
        self.points = points
        self.COLOR = COLOR
        super().__init__(**kwds)

    def move(self, potted):
        super().move(potted)


class WhiteBall(Ball):
    # COLOR = WHITE
    # velocity = Vec2D(0, 0) # 352,-100 - да се подобри сблусъка
    # grabed = False
    # points = 4

    def __init__(self, **kwds):
        self.COLOR = WHITE
        self.grabed = False
        self.points = 4
        super().__init__(**kwds)
        # self.coords = Vec2D(coords)
        # self.pos = Vec2D(coords)
        # self.vizibility = True


class RedBall(Ball):
    # COLOR = RED
    # points = 1

    def __init__(self, **kwds):
        self.COLOR = RED
        self.points = 1
        super().__init__(**kwds)
        # self.coords = Vec2D(coords)
        # self.velocity = velocity
        # self.pos = Vec2D(coords)
        # self.vizibility = True

    def move(self, potted):
        super().move(potted)