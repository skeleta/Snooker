import pygame
from settings import *
import balls
import math
from vec2D import Vec2d as Vec2D
from collections import deque
from cue import Cue


class Game():
    clock = pygame.time.Clock()

    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Cool Snooker')
        self.table = pygame.image.load('Snooker_table3.png')
        self.game_surface = pygame.Surface(SCREEN_SIZE)
        self.white_ball = balls.WhiteBall(POS_WHITE)
        self.redball1 = balls.RedBall(POS_RED1)
        self.redball2 = balls.RedBall(POS_RED2)
        self.redball3 = balls.RedBall(POS_RED3)
        self.redball4 = balls.RedBall(POS_RED4)
        self.redball5 = balls.RedBall(POS_RED5)
        self.redball6 = balls.RedBall(POS_RED6)
        self.redball7 = balls.RedBall(POS_RED7)
        self.redball8 = balls.RedBall(POS_RED8)
        self.redball9 = balls.RedBall(POS_RED9)
        self.redball10 = balls.RedBall(POS_RED10)
        self.redball11 = balls.RedBall(POS_RED11)
        self.redball12 = balls.RedBall(POS_RED12)
        self.redball13 = balls.RedBall(POS_RED13)
        self.redball14 = balls.RedBall(POS_RED14)
        self.redball15 = balls.RedBall(POS_RED15)
        self.black = balls.ColorBall(POS_BLACK, BLACK, 7)
        self.pink = balls.ColorBall(POS_PINK, PINK, 6)
        self.blue = balls.ColorBall(POS_BLUE, BLUE, 5)
        self.brown = balls.ColorBall(POS_BROWN, BROWN, 4)
        self.green = balls.ColorBall(POS_GREEN, GREEN, 3)
        self.yellow = balls.ColorBall(POS_YELLOW, YELLOW, 2)
        self.all_balls = deque([self.redball1, self.redball2, self.redball3,
                                self.redball4, self.redball5, self.redball6,
                                self.redball7, self.redball8, self.redball9,
                                self.redball10, self.redball11, self.redball12,
                                self.redball13, self.redball14, self.redball15,
                                self.white_ball, self.black, self.pink,
                                self.blue, self.brown, self.green, self.yellow])
        self.cue = Cue()

    def ball_update(self):
        for a in range(0, len(self.all_balls)-1):
            for b in range(a+1, len(self.all_balls)):
                ball, next_ball = self.all_balls[a], self.all_balls[b]
                delta = next_ball.coords - ball.coords
                if delta.length <= ball.RADIUS * 2:
                    ball_axis = Vec2D.normalized(Vec2D((-ball.velocity.y, ball.velocity.x)))
                    next_ball_axis = Vec2D.normalized(Vec2D((-next_ball.velocity.y, next_ball.velocity.x)))
                    if ball.velocity.length > 0 and next_ball.velocity.length > 0:
                        ball.coords += Vec2D.normalized(delta) * (delta.length - ball.RADIUS * 2)
                        next_ball.coords += Vec2D.normalized(-delta) * (delta.length - ball.RADIUS * 2)
                        sin = self.sin(ball.velocity, delta)
                        ball.velocity = ball.velocity - 2 * (ball.velocity.dot(ball_axis)) * ball_axis
                        ball.velocity *= sin
                        next_ball.velocity -= 2 * (next_ball.velocity.dot(next_ball_axis)) * next_ball_axis
                        next_ball.velocity *= (1 - sin)
                    elif ball.velocity.length > 0:
                        ball.coords += Vec2D.normalized(delta) * (delta.length - ball.RADIUS * 2)
                        sin = self.sin(ball.velocity, delta)
                        old_velocity = ball.velocity.length
                        ball.velocity -= 2 * (ball.velocity.dot(ball_axis)) * ball_axis
                        ball.velocity *= sin
                        next_ball.velocity = Vec2D.normalized(delta) * old_velocity * (1 - sin)
                    elif next_ball.velocity.length > 0:
                        next_ball.coords += Vec2D.normalized(-delta) * (delta.length - ball.RADIUS * 2)
                        delta = -delta
                        sin = self.sin(next_ball.velocity, delta)
                        old_velocity = next_ball.velocity.length
                        next_ball.velocity -= 2 * (next_ball.velocity.dot(next_ball_axis)) * next_ball_axis
                        next_ball.velocity *= sin
                        ball.velocity = Vec2D.normalized(delta) * old_velocity * (1 - sin)

    def draw_balls(self):
        for ball in self.all_balls:
            balls.Ball._move(ball)
            pygame.draw.circle(self.game_surface, ball.COLOR,\
            (int(ball.coords.x), int(ball.coords.y)), ball.RADIUS)

    def sin(self, velocity, delta):
        prod = velocity.dot(delta)
        cos = prod / (velocity.length * delta.length)
        if cos > 1:
            cos = 1
        if cos ** 2 > 1:
            sin = -math.sqrt((cos ** 2) - 1)
        else:
            sin = math.sqrt(1 - (cos ** 2))
        return sin

    def white_ball_grab(self):
        mouse_pos = Vec2D(pygame.mouse.get_pos())
        if self.white_ball.coords.x-8 < mouse_pos.x < \
                    self.white_ball.coords.x+8 and self.white_ball.coords.y-8\
                    < mouse_pos.y < self.white_ball.coords.y+8:
                for event in pygame.event.get():
                    (mouse1, mouse2, mouse3) = pygame.mouse.get_pressed()
                    if mouse1:
                        self.white_ball.grabed = True
                    else:
                        self.white_ball.grabed = False
        if self.white_ball.grabed:
            self.white_ball.coords = mouse_pos

    def cue_draw(self):
        if self.white_ball.velocity.length == 0:
            start_pos, end_pos = self.cue.get_cue_pos(self.white_ball.coords)
            pygame.draw.line(self.game_surface, self.cue.color, \
            (int(start_pos.x), int(start_pos.y)), (int(end_pos.x),\
            int(end_pos.y)), 3)
