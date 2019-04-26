import random
from typing import List
import itertools
from man.battleships.config import BOARD_SIZE
from man.battleships.game_types import Board
from man.battleships.game_types.Bot import Bot
from man.battleships.game_types.Point import Point
from man.battleships.game_types.Ship import Ship, Orientation


class BackwardBot(Bot):
    """ Hello! I am a dumb sample bot who places their ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.points = (i for i in reversed(list(Point(s[1], s[0]) for s in itertools.product(range(10), range(10)))))


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
                    random.randint(0, BOARD_SIZE), random.randint(0, BOARD_SIZE)
                )

                placements.append((ship, random_point, random_orientation))

            if Board.is_valid_ship_placement(placements):
                break

        return placements

    def get_shot(self):
        """

        :param board:
        :return:
        """

        return next(self.points)

        # return Point(x, y)
