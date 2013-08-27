import unittest
import pygame
import balls
from settings import *
from game import Game
from vec2D import Vec2d as Vec2D
from contextlib import contextmanager


class GameTestWithRedBallsNoBallHitted(unittest.TestCase):
    pygame.init()
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game = None

    def test_non_statick_to_static_board(self):
        self.game.green.velocity = Vec2D(20, 40)
        self.game.if_statick_board()
        self.assertEqual(self.game.board_status, NON_STATICK)
        self.game.green.velocity = Vec2D(0, 0)
        self.game.if_statick_board()
        self.assertEqual(self.game.board_status, STATICK)

    def test_wrong_ball_hit(self):
        self.game.hitted_balls.append(self.game.black)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 7)

    def test_no_ball_hit(self):
        self.game.hit = True
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 4)
        self.assertEqual(self.game.turn, self.game.second_player)
        
        
    def test_statick_board(self):
        self.game.if_statick_board()
        self.assertEqual(self.game.board_status, STATICK)

    def test_ball_potted_hendler(self):
        self.game.yellow.is_potted = True
        self.game.balls_handler()
        self.assertIn(self.game.yellow, self.game.potted)
        self.game.game_handler()
        self.assertNotIn(self.game.yellow, self.game.potted)
        self.assertEqual(self.game.turn.points, FOUL_POINTS)

    def test_two_red_potted(self):
        self.game.redball1.is_potted = True
        self.game.redball2.is_potted = True
        self.game.balls_handler()
        self.game.potted_ball_handler(self.game.potted)
        self.assertNotIn(self.game.redball1, self.game.all_balls)
        self.assertNotIn(self.game.redball2, self.game.all_balls)
        self.assertEqual(self.game.turn.points, 2)

    def test_red_and_color_potted(self):
        self.game.blue.is_potted = True
        self.game.redball1.is_potted = True
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 5)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertNotIn(self.game.redball1, self.game.all_balls)


class GameTestRedballToHit(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.hitted_balls.append(self.game.redball1)

    def tearDown(self):
        self.game = None

    def test_just_white_potted(self):
        self.game.hitted_balls.remove(self.game.redball1)
        self.game.white_ball.is_potted = True
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.first_player.points, 0)

    def test_red_hit_red_potted(self):
        self.game.redball4.is_potted = True
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 1)
        self.assertEqual(self.game.turn.target, COLOR_TARGET)
        self.assertEqual(self.game.second_player.points, 0)
        self.assertFalse(self.game.redball4.is_potted)
        self.assertNotIn(self.game.redball4, self.game.all_balls)

    def test_red_hit_white_potted(self):
        self.game.white_ball.coords = Vec2D(UR_POCKET)
        self.game.white_ball.velocity = Vec2D(10, 50)
        self.assertFalse(self.game.white_ball.is_potted)
        self.game.balls_handler()
        self.assertTrue(self.game.white_ball.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertEqual(self.game.white_ball.coords, Vec2D(POS_WHITE))

    def test_red_hit_white_and_red_potted(self):
        self.game.white_ball.is_potted = True
        self.game.redball3.is_potted = True
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertNotIn(self.game.redball3, self.game.all_balls)

    def test_red_hit_white_and_red_and_color_potted(self):
        self.game.white_ball.coords = Vec2D(UR_POCKET)
        self.game.black.coords = Vec2D(UL_POCKET)
        self.game.white_ball.velocity = Vec2D(10, 50)
        self.game.black.velocity = Vec2D(20, 40)
        self.game.redball2.is_potted = True
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertFalse(self.game.black.is_potted)
        self.game.balls_handler()
        self.assertTrue(self.game.white_ball.is_potted)
        self.assertTrue(self.game.black.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 7)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertEqual(self.game.white_ball.coords, Vec2D(POS_WHITE))
        self.assertEqual(self.game.black.coords, Vec2D(POS_BLACK))
        self.assertNotIn(self.game.redball2, self.game.all_balls)

    def test_red_hit_white_and_color_potted(self):
        self.game.white_ball.coords = Vec2D(DR_POCKET)
        self.game.blue.coords = Vec2D(ML_POCKET)
        self.game.white_ball.velocity = Vec2D(30, 50)
        self.game.blue.velocity = Vec2D(20, 10)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertFalse(self.game.blue.is_potted)
        self.game.balls_handler()
        self.assertTrue(self.game.white_ball.is_potted)
        self.assertTrue(self.game.blue.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 5)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.blue.is_potted)
        self.assertEqual(self.game.white_ball.coords, Vec2D(POS_WHITE))
        self.assertEqual(self.game.blue.coords, Vec2D(POS_BLUE))

    def test_red_hit_color_potted(self):
        self.game.green.coords = Vec2D(DR_POCKET)
        self.game.green.velocity = Vec2D(10, 10)
        self.assertFalse(self.game.green.is_potted)
        self.game.balls_handler()
        self.assertTrue(self.game.green.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.green.is_potted)
        self.assertEqual(self.game.green.coords, Vec2D(POS_GREEN))

    def test_color_hit_just_white_potted(self):
        self.game.hitted_balls.appendleft(self.game.blue)
        self.game.white_ball.coords = Vec2D(DR_POCKET)
        self.game.white_ball.velocity = Vec2D(30, 40)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.turn.points, 5)
        self.assertEqual(self.game.white_ball.coords, Vec2D(POS_WHITE))

    def test_higher_color_hit_lower_color_potted(self):
        self.game.hitted_balls.appendleft(self.game.pink)
        self.game.brown.coords = Vec2D(MR_POCKET)
        self.game.brown.velocity = Vec2D(60, 40)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.turn.points, 6)
        self.assertEqual(self.game.brown.coords, Vec2D(POS_BROWN))

    def test_lower_color_hit_higher_color_potted(self):
        self.game.hitted_balls.appendleft(self.game.green)
        self.game.black.coords = Vec2D(ML_POCKET)
        self.game.black.velocity = Vec2D(50, 40)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.turn.points, 7)
        self.assertEqual(self.game.black.coords, Vec2D(POS_BLACK))

    def test_low_color_hit_low_color_potted(self):
        self.game.hitted_balls.appendleft(self.game.green)
        self.game.brown.coords = Vec2D(MR_POCKET)
        self.game.brown.velocity = Vec2D(60, 40)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.brown.coords, Vec2D(POS_BROWN))

    def test_color_hit_white_and_red_potted(self):
        self.game.hitted_balls.appendleft(self.game.black)
        self.game.white_ball.coords = Vec2D(DR_POCKET)
        self.game.redball4.coords = Vec2D(DL_POCKET)
        self.game.white_ball.velocity = Vec2D(70, 50)
        self.game.redball4.velocity = Vec2D(20, 70)
        self.game.redball8.is_potted = True
        self.assertFalse(self.game.white_ball.is_potted)
        self.game.balls_handler()
        self.assertTrue(self.game.white_ball.is_potted)
        self.assertTrue(self.game.redball4.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 7)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertEqual(self.game.white_ball.coords, Vec2D(POS_WHITE))
        self.assertNotIn(self.game.redball8, self.game.all_balls)
        self.assertNotIn(self.game.redball4, self.game.all_balls)

    def test_color_hit_white_and_red_and_color_potted(self):
        self.game.hitted_balls.appendleft(self.game.black)
        self.game.white_ball.coords = Vec2D(UR_POCKET)
        self.game.pink.coords = Vec2D(UL_POCKET)
        self.game.white_ball.velocity = Vec2D(10, 50)
        self.game.pink.velocity = Vec2D(20, 40)
        self.game.redball8.is_potted = True
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertFalse(self.game.pink.is_potted)
        self.game.balls_handler()
        self.assertTrue(self.game.white_ball.is_potted)
        self.assertTrue(self.game.pink.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 7)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertEqual(self.game.white_ball.coords, Vec2D(POS_WHITE))
        self.assertEqual(self.game.pink.coords, Vec2D(POS_PINK))
        self.assertNotIn(self.game.redball8, self.game.all_balls)

    def test_color_hit_white_and_color_potted(self):
        self.game.hitted_balls.appendleft(self.game.blue)
        self.game.white_ball.coords = Vec2D(UR_POCKET)
        self.game.pink.coords = Vec2D(UL_POCKET)
        self.game.white_ball.velocity = Vec2D(10, 50)
        self.game.pink.velocity = Vec2D(20, 40)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertFalse(self.game.pink.is_potted)
        self.game.balls_handler()
        self.assertTrue(self.game.white_ball.is_potted)
        self.assertTrue(self.game.pink.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 6)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertEqual(self.game.white_ball.coords, Vec2D(POS_WHITE))
        self.assertEqual(self.game.pink.coords, Vec2D(POS_PINK))

    def test_color_hit_red_potted(self):
        self.game.hitted_balls.appendleft(self.game.pink)
        self.game.redball2.coords = Vec2D(UL_POCKET)
        self.game.redball2.velocity = Vec2D(20, 40)
        self.game.balls_handler()
        self.assertTrue(self.game.redball2.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 6)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.redball2.is_potted)
        self.assertNotIn(self.game.redball2, self.game.all_balls)


class GameTestColorBallToHit(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.turn.change_target()

    def tearDown(self):
        self.game = None

    def test_target_change(self):
        self.assertEqual(self.game.turn.target, COLOR_TARGET)
        self.game.hitted_balls.append(self.game.redball1)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertEqual(self.game.turn.target, RED_TARGET)

    def test_color_hit_white_and_red_and_color_potted(self):
        self.game.hitted_balls.appendleft(self.game.black)
        self.game.white_ball.coords = Vec2D(UR_POCKET)
        self.game.pink.coords = Vec2D(UL_POCKET)
        self.game.white_ball.velocity = Vec2D(10, 50)
        self.game.pink.velocity = Vec2D(20, 40)
        self.game.redball8.is_potted = True
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertFalse(self.game.pink.is_potted)
        self.game.balls_handler()
        self.assertTrue(self.game.white_ball.is_potted)
        self.assertTrue(self.game.pink.is_potted)
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 6)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.second_player, self.game.turn)
        self.assertFalse(self.game.white_ball.is_potted)
        self.assertEqual(self.game.white_ball.coords, Vec2D(POS_WHITE))
        self.assertEqual(self.game.pink.coords, Vec2D(POS_PINK))
        self.assertNotIn(self.game.redball8, self.game.all_balls)

    def test_correct_ball_pot(self):
        self.game.yellow.coords = Vec2D(UL_POCKET)
        self.game.yellow.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.turn.points, 2)
        self.assertEqual(self.game.first_player, self.game.turn)
        self.assertEqual(self.game.turn.target, RED_TARGET)
        


class GameTestNoRedBallAtTheTable(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        no_red_balls = []
        for ball in self.game.all_balls:
            if not isinstance(ball, balls.RedBall):
                no_red_balls.append(ball)
        self.game.all_balls = no_red_balls
        self.game.turn.change_target()

    def tearDown(self):
        self.game = None

    def test_condition_change(self):
        self.assertEqual(self.game.turn.target, COLOR_TARGET)
        self.game.hit = True
        self.game.hitted_balls.append(self.game.blue)
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'still red')
        self.assertEqual(self.game.turn.target, RED_TARGET)
        self.assertEqual(self.game.turn.points, 0)
        self.game.hit = True
        self.game.hitted_balls.append(self.game.yellow)
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, 0)

    def test_correct_hit(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.yellow)
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, 0)
        self.assertEqual(self.game.turn, self.game.second_player)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.next_target_ball, 2)

    def test_correct_hit_and_pot(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.yellow)
        self.game.yellow.coords = Vec2D(UL_POCKET)
        self.game.yellow.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, 2)
        self.assertEqual(self.game.turn, self.game.first_player)
        self.assertEqual(self.game.second_player.points, 0)
        self.assertEqual(self.game.next_target_ball, 3)
        self.assertNotIn(self.game.yellow, self.game.all_balls)

    def test_correct_hit_wrong_ball_pot_high(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.yellow)
        self.game.blue.coords = Vec2D(UL_POCKET)
        self.game.blue.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, 5)
        self.assertEqual(self.game.turn, self.game.second_player)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.next_target_ball, 2)
        self.assertIn(self.game.yellow, self.game.all_balls)
        self.assertEqual(self.game.blue.coords, Vec2D(POS_BLUE))

    def test_wrong_hit(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.pink)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, 6)
        self.assertEqual(self.game.next_target_ball, 2)
        self.assertEqual(self.game.turn, self.game.second_player)

    def test_wrong_hit_and_ball_pot(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.green)
        self.game.yellow.coords = Vec2D(UL_POCKET)
        self.game.yellow.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.turn, self.game.second_player)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.next_target_ball, 2)
        self.assertIn(self.game.yellow, self.game.all_balls)
        self.assertEqual(self.game.yellow.coords, Vec2D(POS_YELLOW))

    def test_more_then_one_potted_high(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.yellow)
        self.game.yellow.coords = Vec2D(UL_POCKET)
        self.game.yellow.velocity = Vec2D(10, 50)
        self.game.blue.coords = Vec2D(DL_POCKET)
        self.game.blue.velocity = Vec2D(10, 50)
        self.game.black.coords = Vec2D(UR_POCKET)
        self.game.black.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, 7)
        self.assertEqual(self.game.turn, self.game.second_player)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.next_target_ball, 2)
        self.assertIn(self.game.yellow, self.game.all_balls)
        self.assertEqual(self.game.yellow.coords, Vec2D(POS_YELLOW))
        self.assertEqual(self.game.blue.coords, Vec2D(POS_BLUE))
        self.assertEqual(self.game.black.coords, Vec2D(POS_BLACK))

    def test_wrong_hit_and_ball_pot_high(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.blue)
        self.game.yellow.coords = Vec2D(UL_POCKET)
        self.game.yellow.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, 5)
        self.assertEqual(self.game.turn, self.game.second_player)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.next_target_ball, 2)
        self.assertIn(self.game.yellow, self.game.all_balls)
        self.assertEqual(self.game.yellow.coords, Vec2D(POS_YELLOW))

    def test_wrong_hit_low(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.green)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.next_target_ball, 2)
        self.assertEqual(self.game.turn, self.game.second_player)

    def test_more_then_one_potted_low(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.yellow)
        self.game.yellow.coords = Vec2D(UL_POCKET)
        self.game.yellow.velocity = Vec2D(10, 50)
        self.game.brown.coords = Vec2D(DL_POCKET)
        self.game.brown.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.turn, self.game.second_player)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.next_target_ball, 2)
        self.assertIn(self.game.yellow, self.game.all_balls)
        self.assertEqual(self.game.yellow.coords, Vec2D(POS_YELLOW))
        self.assertEqual(self.game.brown.coords, Vec2D(POS_BROWN))

    def test_correct_hit_wrong_ball_pot_low(self):
        self.game.turn.change_target()
        self.game.hitted_balls.appendleft(self.game.yellow)
        self.game.green.coords = Vec2D(UL_POCKET)
        self.game.green.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, FOUL_POINTS)
        self.assertEqual(self.game.turn, self.game.second_player)
        self.assertEqual(self.game.first_player.points, 0)
        self.assertEqual(self.game.next_target_ball, 2)
        self.assertIn(self.game.yellow, self.game.all_balls)
        self.assertEqual(self.game.green.coords, Vec2D(POS_GREEN))

    def test_game_finish_test(self):
        self.game.turn.change_target()
        self.game.all_balls = [self.game.black]
        self.game.hitted_balls.appendleft(self.game.black)
        self.game.black.coords = Vec2D(UL_POCKET)
        self.game.black.velocity = Vec2D(10, 50)
        while self.game.next_target_ball != 7:
            self.game.next_target_ball = next(self.game.colol_target_order)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.condition, 'red free')
        self.assertEqual(self.game.turn.points, 7)
        self.assertEqual(self.game.turn, self.game.first_player)
        self.assertFalse(self.game.next_target_ball)
        self.assertEqual(self.game.all_balls, [])
        


class GameTestBallReturningTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game = None

    def test_free_self_ball_pos(self):
        self.game.green.coords = Vec2D(UL_POCKET)
        self.game.green.velocity = Vec2D(10, 50)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.green.coords, Vec2D(POS_GREEN))

    def test_self_ball_pos_taken_free_other_color_pos(self):
        self.game.blue.coords = Vec2D(ML_POCKET)
        self.game.pink.coords = Vec2D(POS_GREEN) + 20
        self.game.blue.velocity = Vec2D(10, 50)
        self.game.redball4.coords = Vec2D(POS_BLUE)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.blue.coords, Vec2D(POS_PINK))

    def test_no_free_color_ball_pos(self):
        self.game.black.coords = Vec2D(ML_POCKET)
        self.game.black.velocity = Vec2D(10, 50)
        self.game.redball5.coords = Vec2D(POS_BLACK)
        self.game.balls_handler()
        self.game.game_handler()
        self.assertEqual(self.game.black.coords.x, Vec2D(POS_BLACK).x + 16)
        self.assertEqual(self.game.black.coords.y, Vec2D(POS_BLACK).y)

class GameTestBallMovementAndCollision(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game = None

    def test_moving_ball_to_statick_ball_collision(self):
        self.game.redball1.coords = Vec2D((550, 257))
        self.game.white_ball.coords = Vec2D((650, 250))
        self.game.white_ball.velocity = Vec2D((-140, 0))
        while not self.game.hitted_balls:
            self.game.balls_handler()
            self.game.game_handler()
        self.assertGreater(self.game.redball1.velocity.y, 0)
        self.assertLess(self.game.white_ball.velocity.y, 0)
        self.assertIn(self.game.redball1, self.game.hitted_balls)

    def test_moving_ball_to_statick_ball_collision_white_first(self):
        self.game.all_balls = [self.game.white_ball, self.game.redball1]
        self.game.redball1.coords = Vec2D((550, 257))
        self.game.white_ball.coords = Vec2D((650, 250))
        self.game.white_ball.velocity = Vec2D((-140, 0))
        while not self.game.hitted_balls:
            self.game.balls_handler()
            self.game.game_handler()
        self.assertGreater(self.game.redball1.velocity.y, 0)
        self.assertLess(self.game.white_ball.velocity.y, 0)
        self.assertIn(self.game.redball1, self.game.hitted_balls)

    def test_moving_to_moving_ball_collision(self):
        self.game.redball1.coords = Vec2D((550, 257))
        self.game.white_ball.coords = Vec2D((650, 250))
        self.game.redball1.velocity = Vec2D((40, 0))
        self.game.white_ball.velocity = Vec2D((-140, 0))
        while self.game.redball1.velocity.y == 0:
            self.game.balls_handler()
            self.game.game_handler()
        self.assertGreater(self.game.redball1.velocity.y, 0)
        self.assertLess(self.game.white_ball.velocity.y, 0)

    def test_cue(self):
        self.game.cue.r = CUE_DEFAULT_R * 2
        self.game.game_handler()
        self.assertEqual(self.game.cue.r, CUE_DEFAULT_R + CUE_DEFAULT_R/2)
        self.game.cue.r = 0
        self.game.game_handler()
        self.assertEqual(self.game.cue.r, CUE_DEFAULT_R)
        
        

if __name__ == '__main__':
    unittest.main()
