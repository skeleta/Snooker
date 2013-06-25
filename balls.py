import pygame
from settings import *
from vec2D import Vec2d as Vec2D


class Ball():
    RADIUS = 8
    pocket_area = False

    def __init__(self, coords, COLOR, points=0, velocity=Vec2D(0, 0)):
        self.coords = Vec2D(coords)
        self.points = points
        self.COLOR = COLOR
        self.velocity = velocity

    def _move(ball, pockets):
        check = Vec2D(ball.velocity)
        ball.velocity -= Vec2D.normalized(ball.velocity) * FRICTION * TIMER
        ball.coords += ball.velocity * TIMER
        if check.x * ball.velocity.x < 0:
            ball.velocity = Vec2D(0, 0)
        ball.pocket_area = False
        for pocket in pockets:
            delta = ball.coords - pockets[pocket][0]
            if delta.length <= POCKET_R2:
                print(pocket)
                if delta.length <= POCKET_R:
                    print('kabuum')
                ball.pocket_area = True
        if ball.pocket_area:
            if ball.coords.x < LEFT_BORDER-13 or ball.coords.x > RIGHT_BORDER+13:
                ball.velocity.x = -ball.velocity.x
            elif ball.coords.y < UP_BORDER-13 or ball.coords.y > DOWN_BORDER+13:
                ball.velocity.y = -ball.velocity.y
        else:
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
    velocity = Vec2D(160, -120) # 352,-100 - да се подобри сблусъка
    grabed = False

    def __init__(self, coords):
        self.coords = Vec2D(coords)


class RedBall(Ball):
    COLOR = RED
    points = 1

    def __init__(self, coords, velocity=Vec2D(0, 0)):
        self.coords = Vec2D(coords)
        self.velocity = velocity
