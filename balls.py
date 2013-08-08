import pygame
import math
from settings import *
from vec2D import Vec2d as Vec2D


class Ball():
    RADIUS = 8
    potted = []

    def __init__(self, coords, COLOR, points=0, velocity=Vec2D(0, 0)):
        self.coords = Vec2D(coords)
        self.points = points
        self.COLOR = COLOR
        self.velocity = velocity
        self.vizibility = True

    def _move(ball, pockets):
        check = Vec2D(ball.velocity)
        ball.velocity -= Vec2D.normalized(ball.velocity) * FRICTION * TIMER
        ball.coords += ball.velocity * TIMER
        if check.x * ball.velocity.x < 0:
            ball.velocity = Vec2D(0, 0)
        if int(ball.coords.x) not in range(139, 534) and\
                int(ball.coords.x) not in range(564, 960)\
                and int(ball.coords.y) not in range(90, 484):

            """Ако някоя от топките е в обсега на някой от джобовете
            влизаме в този if и почваме да следим за сблъсък със стената на
            някой от джобовете или за попадение в джоба"""

            for pocket in pockets:
                Ball.pocket_walls_collision(ball, pockets[pocket][1], pockets[pocket][2])
                Ball.pocket_walls_collision(ball, pockets[pocket][3], pockets[pocket][4])
                if (ball.coords - pockets[pocket][0]).length <= POCKET_R:
                    if ball not in Ball.potted:
                        Ball.potted.append(ball)
                        ball.vizibility = False
                        ball.coords = Vec2D(1000, 1000) + ball.pos
                        ball.velocity = Vec2D(0, 0)
        else:
            if ball.coords.x < LEFT_BORDER or ball.coords.x > RIGHT_BORDER:
                ball.velocity.x = -ball.velocity.x
            elif ball.coords.y < UP_BORDER or ball.coords.y > DOWN_BORDER:
                ball.velocity.y = -ball.velocity.y

    def pocket_walls_collision(ball, start_point, end_point):
        incoming_vec = ball.coords - start_point
        pocket_wall_vec = end_point - start_point
        projected = Vec2D.projection(incoming_vec, pocket_wall_vec)
        distance = Vec2D.get_distance(incoming_vec, projected)
        if 0 <= math.fabs(projected.x) <=\
                math.fabs(end_point.x - start_point.x) and\
                0 <= math.fabs(projected.y) <=\
                math.fabs(end_point.y - start_point.y) and\
                distance < ball.RADIUS:
            ball.coords = Vec2D.normalized(incoming_vec - projected) *\
                          ball.RADIUS + start_point + projected
            ball.velocity = 2 * (ball.velocity.dot(pocket_wall_vec) /\
                            pocket_wall_vec.dot(pocket_wall_vec)) *\
                            pocket_wall_vec - ball.velocity

    # def _ball_update(all_balls):
    #     for a in range(0, len(all_balls)-1):
    #         for b in range(a+1, len(all_balls)):
    #             ball, next_ball = all_balls[a], all_balls[b]
    #             delta = next_ball.coords - ball.coords
    #             if delta.length <= ball.RADIUS * 2:
    #                 ball_axis = Vec2D.perpendicular_normal(ball.velocity)
    #                 next_ball_axis = Vec2D.perpendicular_normal(next_ball.velocity)
    #                 if ball.velocity.length > 0 and next_ball.velocity.length > 0:
    #                     ball.coords += Vec2D.normalized(delta) * (delta.length - ball.RADIUS * 2)
    #                     next_ball.coords += Vec2D.normalized(-delta) * (delta.length - ball.RADIUS * 2)
    #                     sin = -math.sin(math.radians(Vec2D.get_angle_between(ball.velocity, delta)))
    #                     ball.velocity -= 2 * (ball.velocity.dot(ball_axis)) * ball_axis
    #                     ball.velocity *= sin
    #                     next_ball.velocity -= 2 * (next_ball.velocity.dot(next_ball_axis)) * next_ball_axis
    #                     next_ball.velocity *= (1 - sin)
    #                 elif ball.velocity.length > 0:
    #                     ball.coords += Vec2D.normalized(delta) * (delta.length - ball.RADIUS * 2)
    #                     sin = -math.sin(math.radians(Vec2D.get_angle_between(ball.velocity, delta)))
    #                     old_velocity = ball.velocity.length
    #                     ball.velocity -= 2 * (ball.velocity.dot(ball_axis)) * ball_axis
    #                     ball.velocity *= sin
    #                     next_ball.velocity = Vec2D.normalized(delta) * old_velocity * (1 - sin)
    #                 elif next_ball.velocity.length > 0:
    #                     next_ball.coords += Vec2D.normalized(-delta) * (delta.length - ball.RADIUS * 2)
    #                     delta = -delta
    #                     sin = -math.sin(math.radians(Vec2D.get_angle_between(next_ball.velocity, delta)))
    #                     old_velocity = next_ball.velocity.length
    #                     next_ball.velocity -= 2 * (next_ball.velocity.dot(next_ball_axis)) * next_ball_axis
    #                     next_ball.velocity *= sin
    #                     ball.velocity = Vec2D.normalized(delta) * old_velocity * (1 - sin)



class ColorBall(Ball):
    def __init__(self, coords, COLOR, points, velocity=Vec2D(0, 0)):
        self.coords = Vec2D(coords)
        self.pos = Vec2D(coords)
        self.points = points
        self.COLOR = COLOR
        self.velocity = velocity
        self.vizibility = True


class WhiteBall(Ball):
    COLOR = WHITE
    velocity = Vec2D(0, 0) # 352,-100 - да се подобри сблусъка
    grabed = False
    vizibility = True
    points = 4

    def __init__(self, coords):
        self.coords = Vec2D(coords)
        self.pos = Vec2D(coords)


class RedBall(Ball):
    COLOR = RED
    points = 1

    def __init__(self, coords, velocity=Vec2D(0, 0)):
        self.coords = Vec2D(coords)
        self.velocity = velocity
        self.pos = Vec2D(coords)
        self.vizibility = True
