import pygame
from settings import *
import balls
import math
from vec2D import Vec2d as Vec2D
from collections import deque
from cue import Cue
from score import Score
from player import Player
from draw import Draw


class Game():
    clock = pygame.time.Clock()
    pockets = {'ur_pocket': [Vec2D(UR_POCKET), Vec2D(125, 94), Vec2D(113, 78),
                             Vec2D(143, 75), Vec2D(128, 63)],
               'ul_pocket': [Vec2D(UL_POCKET), Vec2D(125, 480),
                             Vec2D(113, 495), Vec2D(143, 498),
                             Vec2D(128, 510)],
               'dl_pocket': [Vec2D(DL_POCKET), Vec2D(974, 480),
                             Vec2D(986, 495), Vec2D(956, 498),
                             Vec2D(971, 510)],
               'dr_pocket': [Vec2D(DR_POCKET), Vec2D(956, 75), Vec2D(971, 63),
                             Vec2D(974, 94), Vec2D(986, 79)],
               'ml_pocket': [Vec2D(ML_POCKET), Vec2D(530, 498),
                             Vec2D(539, 510), Vec2D(568, 498),
                             Vec2D(560, 510)],
               'mr_pocket': [Vec2D(MR_POCKET), Vec2D(530, 75), Vec2D(539, 63),
                             Vec2D(568, 75), Vec2D(560, 63)]}

    def __init__(self):
        self.moving_balls = deque([])
        self.hitted_balls = deque([])
        self.potted = []
        pygame.display.set_caption('Cool Snooker')
        self.table = pygame.image.load('Snooker_table3.png')
        self.white_ball = balls.WhiteBall(coords=POS_WHITE)
        self.redball1 = balls.RedBall(coords=POS_RED1)
        self.redball2 = balls.RedBall(coords=POS_RED2)
        self.redball3 = balls.RedBall(coords=POS_RED3)
        self.redball4 = balls.RedBall(coords=POS_RED4)
        self.redball5 = balls.RedBall(coords=POS_RED5)
        self.redball6 = balls.RedBall(coords=POS_RED6)
        self.redball7 = balls.RedBall(coords=POS_RED7)
        self.redball8 = balls.RedBall(coords=POS_RED8)
        self.redball9 = balls.RedBall(coords=POS_RED9)
        self.redball10 = balls.RedBall(coords=POS_RED10)
        self.redball11 = balls.RedBall(coords=POS_RED11)
        self.redball12 = balls.RedBall(coords=POS_RED12)
        self.redball13 = balls.RedBall(coords=POS_RED13)
        self.redball14 = balls.RedBall(coords=POS_RED14)
        self.redball15 = balls.RedBall(coords=POS_RED15)
        self.black = balls.ColorBall(coords=POS_BLACK, COLOR=BLACK, points=7)
        self.pink = balls.ColorBall(coords=POS_PINK, COLOR=PINK, points=6)
        self.blue = balls.ColorBall(coords=POS_BLUE, COLOR=BLUE, points=5)
        self.brown = balls.ColorBall(coords=POS_BROWN, COLOR=BROWN, points=4)
        self.green = balls.ColorBall(coords=POS_GREEN, COLOR=GREEN, points=3)
        self.yellow = balls.ColorBall(coords=POS_YELLOW,
                                      COLOR=YELLOW, points=2)
        self.first_player = Player("Selby")
        self.second_player = Player("O'Sullivan")
        self.all_balls = deque([
                               self.redball1, self.redball2, self.redball3,
                               self.redball4, self.redball5, self.redball6,
                               self.redball7, self.redball8, self.redball9,
                               self.redball10, self.redball11, self.redball12,
                               self.redball13, self.redball14, self.redball15,
                               self.white_ball, self.black, self.pink,
                               self.blue, self.brown, self.green, self.yellow
                               ])
        self.cue = Cue()
        self.turn = self.first_player
        self.board_status = STATICK
        self.colol_order = iter([x for x in range(2, 8)])
        self.next_target_ball = next(self.colol_order)
        self.condition = STILL_RED
        self.score = Score()
        self.foul = False
        self.hit = False
        self.painter = Draw()

    def ball_update(self):
        for a in range(0, len(self.all_balls)-1):
            for b in range(a+1, len(self.all_balls)):
                ball, next_ball = self.all_balls[a], self.all_balls[b]
                delta = next_ball.coords - ball.coords
                if (next_ball.coords - ball.coords).length <= ball.RADIUS * 2:
                    if ball.velocity.length > 0 and \
                            next_ball.velocity.length > 0:
                        ball.coords += Vec2D.normalized(delta) *\
                            (delta.length - ball.RADIUS * 2)
                        next_ball.coords += Vec2D.normalized(-delta) *\
                            (delta.length - ball.RADIUS * 2)
                        self.ball_collision(ball, next_ball)
                    elif ball.velocity.length > 0:
                        if isinstance(ball, balls.WhiteBall):
                            self.hitted_balls.append(next_ball)
                        ball.coords += Vec2D.normalized(delta) *\
                            (delta.length - ball.RADIUS * 2)
                        self.ball_collision(ball, next_ball)
                    elif next_ball.velocity.length > 0:
                        if isinstance(next_ball, balls.WhiteBall):
                            self.hitted_balls.append(ball)
                        next_ball.coords += Vec2D.normalized(-delta) *\
                            (delta.length - ball.RADIUS * 2)
                        self.ball_collision(ball, next_ball)

    def balls_handler(self):
        for ball in self.all_balls:
            if ball.velocity.length > 0:
                ball.move(self.pockets)
            if ball.is_potted and ball not in self.potted:
                self.potted.append(ball)
            if ball.vizibility:
                self.painter.draw_balls(ball)

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

    def cue_handler(self):
        start_pos, end_pos = self.cue.get_cue_pos(self.white_ball.coords)
        self.painter.cue_draw(self.cue, start_pos, end_pos)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP_ENTER]:
            new_velocity = Vec2D.normalized(start_pos - end_pos)
            force = Vec2D(self.white_ball.coords - start_pos).length
            self.white_ball.velocity = new_velocity *\
                force ** 2 / MIN_HITTING_FORCE
            self.hit = True
            self.who_plays()

    def if_statick_board(self):
        for ball in self.all_balls:
            if ball.velocity.length > 0 and ball not in self.moving_balls:
                self.moving_balls.append(ball)
            elif ball in self.moving_balls and ball.velocity.length == 0:
                self.moving_balls.remove(ball)
        if not self.moving_balls:
            self.board_status = STATICK
        else:
            self.board_status = NON_STATICK

    def potted_ball_handler(self, potted, color_points=None):
        red_ball = 0
        color_ball = 0
        points = 0
        if color_points is None:
            color_points = [0]
        else:
            color_points = color_points
        for ball in potted:
            if isinstance(ball, balls.WhiteBall):
                self.foul = True
            if isinstance(ball, balls.ColorBall):
                color_ball += 1
                color_points.append(ball.points)
                if self.turn.target != COLOR_TARGET:
                    self.foul = True
            if isinstance(ball, balls.RedBall):
                if self.turn.target != RED_TARGET:
                    self.foul = True
                red_ball += 1
                points += ball.points
            ball.velocity = Vec2D(0, 0)
            if isinstance(ball, balls.RedBall):
                self.all_balls.remove(ball)
                ball.is_potted = False
            else:
                self.ball_return(ball)
            ball.is_potted = False
        self.potted = []
        if color_ball > 1 or (red_ball > 0 and color_ball > 0):
            self.foul = True
        if self.foul is True:
            # print("Foul wrong ball potted")
            self.change_turn()
            if max(color_points) > FOUL_POINTS:
                self.turn.points += max(color_points)
            else:
                self.turn.points += FOUL_POINTS
        else:
            if self.turn.target == RED_TARGET:
                self.turn.points += points
            else:
                self.turn.points += max(color_points)
            self.turn.change_target()

    def game_handler(self):
        self.score.show_score(self.first_player, self.second_player, self.turn)
        self.ball_update()
        self.if_statick_board()
        self.check_condition()
        self.foul = False
        if self.board_status == STATICK:
            if not self.hitted_balls and self.hit is True and not self.potted:
                self.change_turn()
                self.turn.points += FOUL_POINTS
                # print("Foul no ball hit")
            self.hit = False
            self.cue_handler()
            if self.hitted_balls:
                if self.condition == STILL_RED:
                    if (isinstance(self.hitted_balls[0], balls.ColorBall)
                            and self.turn.target != COLOR_TARGET) or\
                            (isinstance(self.hitted_balls[0], balls.RedBall)
                             and self.turn.target != RED_TARGET):
                        if not self.potted:
                            self.foul = True
                            self.change_turn()
                            # print("Foul wrong ball hit")
                            if self.hitted_balls[0].points > FOUL_POINTS:
                                self.turn.points += self.hitted_balls[0].points
                            else:
                                self.turn.points += FOUL_POINTS
                        else:
                            self.foul = True
                            points = [self.hitted_balls[0].points]
                            self.potted_ball_handler(self.potted,
                                                     color_points=points)
                    if self.potted and self.foul is not True:
                        self.potted_ball_handler(self.potted)
                    elif self.foul is not True:
                        # print("No ball poted")
                        self.change_turn()
                else:
                    self.no_red_game_handler()
                self.hitted_balls = deque([])
            if self.potted:
                self.potted_ball_handler(self.potted)

    def change_turn(self):
        if self.turn == self.first_player:
            self.turn = self.second_player
        else:
            self.turn = self.first_player
        self.turn.target = RED_TARGET

    def who_plays(self):
        print("-----")
        print(self.turn.name + " hit")

    def ball_return(self, potted_ball):
        potted_ball.vizibility = True
        returning_pos = Vec2D(potted_ball.pos)
        color_balls_pos = [x.pos for x in self.all_balls
                           if isinstance(x, balls.ColorBall)]
        empty_place = False
        my_place_taken = self.chek_for_place(potted_ball)
        if my_place_taken is True:
            for position in color_balls_pos:
                empty_position = self.chek_for_place(potted_ball, pos=position)
                if empty_position is not True:
                    empty_place = True
                    returning_pos = position
                    break
        if my_place_taken is True and empty_place is not True:
            found_place = False
            while found_place is not True:
                flag = self.chek_for_place(potted_ball, pos=returning_pos)
                if flag is not True:
                    found_place = True
                    break
                returning_pos.x += 1
            potted_ball.coords = returning_pos
        else:
            potted_ball.coords = returning_pos

    def chek_for_place(self, potted_ball, pos=None):
        if pos is None:
            pos = potted_ball.pos
        for ball in self.all_balls:
            if ball is not potted_ball:
                delta = ball.coords - pos
                if delta.length < ball.RADIUS * 2:
                    return True
        return False

    def check_condition(self):
        flag = True
        for ball in self.all_balls:
            if isinstance(ball, balls.RedBall):
                flag = False
                break
        if flag:
            if self.turn.target == COLOR_TARGET:
                self.condition = STILL_RED
            else:
                self.condition = RED_FREE

    def no_red_game_handler(self):
        points = [0]
        if self.hitted_balls[0].points == self.next_target_ball:
            if self.potted:
                if len(self.potted) > 1:
                    # print("Foul more then 1 colorball potted")
                    self.change_turn()
                    for ball in self.potted:
                        points.append(ball.points)
                        self.ball_return(ball)
                        ball.is_potted = False
                    self.potted = []
                    if max(points) > FOUL_POINTS:
                        self.turn.points += max(points)
                    else:
                        self.turn.points += FOUL_POINTS
                else:
                    if self.potted[0].points == self.next_target_ball:
                        self.turn.points += self.potted[0].points
                        self.all_balls.remove(self.potted[0])
                        try:
                            self.next_target_ball = next(self.colol_order)
                        except:
                            self.next_target_ball = False
                            # print("Game finished")
                    else:
                        # print("Foul wrong colorball potted")
                        self.change_turn()
                        if self.potted[0].points > FOUL_POINTS:
                            self.turn.points += self.potted[0].points
                        else:
                            self.turn.points += FOUL_POINTS
                        self.ball_return(self.potted[0])
                    self.potted[0].is_potted = False
                    self.potted.remove(self.potted[0])
            else:
                # print("No colorball potted")
                self.change_turn()
        else:
            # print("Foul wrong colorball hited")
            self.change_turn()
            if self.potted:
                for ball in self.potted:
                    points.append(ball.points)
                    self.ball_return(ball)
                    ball.is_potted = False
                self.potted = []
                points.append(self.hitted_balls[0].points)
                if max(points) > FOUL_POINTS:
                    self.turn.points += max(points)
                else:
                    self.turn.points += FOUL_POINTS
            else:
                if self.hitted_balls[0].points > FOUL_POINTS:
                    self.turn.points += self.hitted_balls[0].points
                else:
                    self.turn.points += FOUL_POINTS

    def ball_collision(self, ball, next_ball):
        delta = next_ball.coords - ball.coords
        unit_delta = Vec2D(delta/delta.get_length())
        unit_tangent = Vec2D(unit_delta.perpendicular())
        velocity_1_n = unit_delta.dot(ball.velocity)
        velocity_1_t = unit_tangent.dot(ball.velocity)
        velocity_2_n = unit_delta.dot(next_ball.velocity)
        velocity_2_t = unit_tangent.dot(next_ball.velocity)
        new_velocity_1_t = velocity_1_t
        new_velocity_2_t = velocity_2_t
        new_velocity_1_n = velocity_2_n
        new_velocity_2_n = velocity_1_n
        new_velocity_1_n = Vec2D(new_velocity_1_n * unit_delta)
        new_velocity_2_n = Vec2D(new_velocity_2_n * unit_delta)
        new_velocity_1_t = Vec2D(new_velocity_1_t * unit_tangent)
        new_velocity_2_t = Vec2D(new_velocity_2_t * unit_tangent)
        new_velocity_1 = Vec2D(new_velocity_1_n + new_velocity_1_t)
        new_velocity_2 = Vec2D(new_velocity_2_n + new_velocity_2_t)
        ball.velocity = new_velocity_1
        next_ball.velocity = new_velocity_2
