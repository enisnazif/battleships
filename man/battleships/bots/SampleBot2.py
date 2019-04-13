import random
from man.battleships.types.Bot import Bot
from man.battleships.types.Ship import Ship, Orientation
from man.battleships.types.Point import Point
from typing import List
from man.battleships.config import BOARD_SIZE

class SampleBot2(Bot):

    """ Hello! I am a dumb sample bot who places their ships randomly and shoots randomly! """

    def place_ships(self, ships: List[Ship]):
        """
        Returns a set of point at which a ship will be placed

        :param ships:
        :return: List[Tuple[Ship, Point, Orientation]]
        """

        placements = []

        for ship in ships:
            random_orientation = random.choice(list(Orientation))
            random_point = Point(random.randint(0, BOARD_SIZE), random.randint(0, BOARD_SIZE))
            placements.append((ship, random_point, random_orientation))

        return placements

    def get_shot(self, board):
        x = random.randint(0, BOARD_SIZE-1)
        y = random.randint(0, BOARD_SIZE-1)

        return Point(x, y)
