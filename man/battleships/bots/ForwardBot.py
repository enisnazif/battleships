import itertools

import random
from typing import List

from man.battleships.config import BOARD_SIZE
from man.battleships.game_types import Board
from man.battleships.game_types.Bot import Bot
from man.battleships.game_types.Point import Point
from man.battleships.game_types.Ship import Ship, Orientation


class ForwardBot(Bot):
    """ Hello! I am a dumb sample bot who shoots sequentially from (0,0) to (9,9) """

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.points = (Point(s[1], s[0]) for s in itertools.product(range(BOARD_SIZE), range(BOARD_SIZE)))

    def get_ship_placements(self, ships: List[Ship]):
        """
        Returns a set of point at which a ship will be placed

        :param ships:
        :return: List[Tuple[Ship, Point, Orientation]]
        """

        while True:
            placements = []
            for ship in ships:
                random_orientation = random.choice(list(Orientation))
                random_point = Point(
                    random.randrange(0, BOARD_SIZE), random.randrange(0, BOARD_SIZE)
                )

                placements.append((ship, random_point, random_orientation))

            if Board.is_valid_ship_placement(placements):
                break

        return placements

    def get_shot(self):
        return next(self.points)
