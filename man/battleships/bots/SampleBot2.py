import random
from man.battleships.types.Bot import Bot
from man.battleships.types.Ship import Ship, Orientation
from man.battleships.types.Point import Point
from typing import List
from man.battleships.config import BOARD_SIZE


class SampleBot2(Bot):
    """ Hello! I am a dumb sample bot who places their ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []

    def place_ships(self, ships: List[Ship]):
        """
        Returns a set of point at which a ship will be placed

        :param ships:
        :return: List[Tuple[Ship, Point, Orientation]]
        """

        for ship in ships:

            while True:

                random_orientation = random.choice(list(Orientation))
                random_point = Point(
                    random.randint(0, BOARD_SIZE), random.randint(0, BOARD_SIZE)
                )

                if self.is_valid_ship_placement(ship, random_point, random_orientation):
                    self.board.place_ship(ship, random_point, random_orientation)
                    break

        return self.board.ship_locations

    def get_shot(self):
        """

        :param board:
        :return:
        """

        # self.board._ship_locations = []

        # Get the status of your last shot - could be useful in planning your next move!
        last_shot_status = self.last_shot_status

        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE - 1)

        while Point(x, y) in self.my_shots:
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - 1)

        self.my_shots.append(Point(x, y))

        return Point(x, y)
