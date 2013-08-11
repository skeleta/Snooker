import unittest
from settings import *
from game import Game
from vec2D import Vec2d as Vec2D


class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game = None

    def test_check_board_sttatus(self):
        self.game.green.velocity = Vec2D(20, 40)
        self.game.if_statick_board()
        self.assertEqual(self.game.board_status, NON_STATICK)
        
    def test_check_board_sttatus_2(self):
        self.game.if_statick_board()
        self.assertEqual(self.game.board_status, STATICK)

if __name__ == '__main__':
    unittest.main()
