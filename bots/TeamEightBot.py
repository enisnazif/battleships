import random
from typing import List, Dict, Union, Tuple

from config import BOARD_SIZE
from game_types import Bot, Board, Point, Ship, ShipType, Orientation


class TeamEightBot(Bot):
    """ Hello! I am a dumb sample bot who places its ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.grid = [[0.01 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

    def get_ship_placements(self, ships: List[Ship]) -> List[Tuple[Ship, Point, Orientation]]:
        """
        Returns a set of point at which a ship will be placed. For each ship, you must return a tuple of [Ship, Point, Orientation],
        where Point corresponds to the bottom left corner of the Ship, e.g:

                     -
        x - - -  or  -
                     -
                     x

        and Orientation is one of Orientation.Vertical and Orientation.Horizontal

        :param ships: A List of Ship which your bot should return placements for
        :return: A list of placements for each ship in 'ships'
        """

        # Perform random ship placement
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

    def get_shot(self) -> Point:
        """
        Called each round by the game engine to get the next point to shoot on the opponents board.

        :return: The next point to shoot on the opponents board
        """

        # Get the status of your last shot - could be useful in planning your next move!
        last = self.last_shot_status

        # Example response:

        # {
        #    'shot': Point(4, 5),                                # type: Point
        #    'is_hit': True,                                     # type: bool
        #    'is_sunk' True,                                     # type: bool
        #    'ship_sunk': <ShipType.Battleship: 'Battleship'>,   # type: ShipType
        #    'error': None                                       # type: Union[None, Exception]
        # }

        if last is not None and last.get('shot') is not None:
            # Don't pick last shot again
            self.grid[last['shot'].x][last['shot'].y] = 0.

            # If was a hit, increase likelihood in neighbours
            if last['is_hit']:
                x, y = last['shot']
                points = [
                    (x - 1, y),
                    (x + 1, y),
                    (x, y - 1),
                    (x, y + 1),
                ]
                for x, y in points:
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                        self.grid[x][y] *= 100.

        # Pick next shot based on likelihoods
        choices = []
        weights = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                point = Point(x, y)
                weight = self.grid[x][y]
                if weight > 0:
                    choices.append(point)
                    weights.append(weight)

        choice = random.choices(choices, weights)[0]
        return choice
