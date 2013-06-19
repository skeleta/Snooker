import pygame
from settings import *
from vec2D import Vec2d as Vec2D


class Ball():
    RADIUS = 8

    def __init__(self, coords, COLOR, points=0, velocity=Vec2D(0, 0)):
        self.coords = Vec2D(coords)
        self.points = points
        self.COLOR = COLOR
        self.velocity = velocity

    def _move(ball):
        if ball.velocity.length > 0:
            check = Vec2D(ball.velocity)
            ball.velocity -= Vec2D.normalized(ball.velocity) * FRICTION * TIMER
            ball.coords += ball.velocity * TIMER
            if check.x * ball.velocity.x < 0:
                ball.velocity = Vec2D(0, 0)
            if ball.coords.x < LEFT_BORDER or ball.coords.x > RIGHT_BORDER:
                ball.velocity.x = -ball.velocity.x
            elif ball.coords.y < UP_BORDER or ball.coords.y > DOWN_BORDER:
                ball.velocity.y = -ball.velocity.y


class ColorBall(Ball):
    def __init__(self, coords, COLOR, points, velocity=Vec2D(0, 0)):
        self.coords = Vec2D(coords)
        self.points = points
        self.COLOR = COLOR
        self.velocity = velocity


class WhiteBall(Ball):
    COLOR = WHITE
    velocity = Vec2D(300, -100)
    grabed = False

    def __init__(self, coords):
        self.coords = Vec2D(coords)


class RedBall(Ball):
    COLOR = RED
    points = 1

    def __init__(self, coords, velocity=Vec2D(0, 0)):
        self.coords = Vec2D(coords)
        self.velocity = velocity
