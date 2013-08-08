from settings import *


class Player():
    points = 150

    def __init__(self, name):
        self.name = name
        self.target = RED_TARGET

    def change_target(self):
        if self.target == RED_TARGET:
            self.target = COLOR_TARGET
        else:
            self.target = RED_TARGET
