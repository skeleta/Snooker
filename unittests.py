import unittest
import pygame
from settings import *
from game import Game
from vec2D import Vec2d as Vec2D


class GameTestWithRedBalls(unittest.TestCase):
    pygame.init()
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game = None

    def test_non_statick_board(self):
        self.game.green.velocity = Vec2D(20, 40)
        self.game.if_statick_board()
        self.assertEqual(self.game.board_status, NON_STATICK)
        
    def test_statick_board(self):
        self.game.if_statick_board()
        self.assertEqual(self.game.board_status, STATICK)

    def test_ball_potted_hendler(self):
        self.game.yellow.is_potted = True
        self.game.draw_balls()
        self.assertIn(self.game.yellow, self.game.potted)
        self.game.game_handler()
        self.assertNotIn(self.game.yellow, self.game.potted)
        self.assertEqual(self.game.turn.points, FOUL_POINTS)

    def test_two_red_potted(self):
        self.game.potted = [self.game.redball1, self.game.redball2]
        self.game.potted_ball_handler(self.game.potted)
        self.assertNotIn(self.game.redball1, self.game.all_balls)
        self.assertNotIn(self.game.redball2, self.game.all_balls)
        self.assertEqual(self.game.turn.points, 2)

    def test_red_and_color_potted(self):
        self.game.blue.is_potted = True
        self.game.redball1.is_potted = True
        self.game.game_handler()
        self.game.draw_balls()
        self.game.game_handler()
        #self.game.potted = [self.game.blue, self.game.redball1]
        #self.game.potted_ball_handler(self.game.potted)
        self.assertEqual(self.game.turn.points, 5)
        self.assertEqual(self.game.firs_player.points, 0)
        

if __name__ == '__main__':
    unittest.main()
