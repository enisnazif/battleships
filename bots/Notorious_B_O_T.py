import random
from typing import List, Dict, Union, Tuple

from config import BOARD_SIZE
from game_types import Bot, Board, Point, Ship, ShipType, Orientation


class Notorious_B_O_T(Bot):
    """ Hello! I am a dumb sample bot who places its ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.map = [[''] * 10 for i in range(10)]

        self.seenX = [0] * 10
        self.seenY = [0] * 10

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

        ships = sorted(ships, key=lambda x: len(x.horizontal_offsets))
        placed = [
          (ships[0], Point(0, 6), Orientation.Horizontal),
          (ships[1], Point(1, 1), Orientation.Vertical),
          (ships[2], Point(6, 2), Orientation.Horizontal),
          (ships[3], Point(3, 8), Orientation.Horizontal),
          (ships[4], Point(1, 5), Orientation.Horizontal),
        ]

        return placed

#        # Perform random ship placement
#        while True:
#            placements = []
#            for ship in ships:
#                random_orientation = random.choice(list(Orientation))
#                random_point = Point(
#                    random.randrange(0, BOARD_SIZE), random.randrange(0, BOARD_SIZE)
#                )
#
#                placements.append((ship, random_point, random_orientation))
#
#            if Board.is_valid_ship_placement(placements):
#                break
#
#        return placements

    def get_best_shot(self):
        squares = [] # tuple of (x, y, score)
        bestScore = -999999
        best = []
        for x in range(10):
          for y in range(10):
            score = 0

            if self.map[x][y]: # if we've already fired at this square, skip
              continue
            if x > 0 and self.map[x-1][y] == 'H':
              score += 10
            if x < 9 and self.map[x+1][y] == 'H':
              score += 10
            if y > 0 and self.map[x][y-1] == 'H':
              score += 10
            if y < 9 and self.map[x][y+1] == 'H':
              score += 10

            score -= self.seenX[x]
            score -= self.seenY[y]

            if ((x == 0 or self.map[x-1][y] == 'M') and
                (x == 9 or self.map[x+1][y] == 'M') and
                (y == 0 or self.map[x][y-1] == 'M') and
                (y == 9 or self.map[x][y+1] == 'M')):
              score -= 10

            if score == bestScore:
              best.append(Point(x, y))

            if score > bestScore:
              bestScore = score
              best = [Point(x, y)]

        return random.sample(best, 1)[0]

    def get_shot(self) -> Point:
        """
        Called each round by the game engine to get the next point to shoot on the opponents board.

        :return: The next point to shoot on the opponents board
        """

        # Get the status of your last shot - could be useful in planning your next move!
        last_shot_status = self.last_shot_status

        # Example response:

        # {
        #    'shot': Point(4, 5),                                # type: Point
        #    'is_hit': True,                                     # type: bool
        #    'is_sunk' True,                                     # type: bool
        #    'ship_sunk': <ShipType.Battleship: 'Battleship'>,   # type: ShipType
        #    'error': None                                       # type: Union[None, Exception]
        # }

        if last_shot_status['shot'] is not None:
          lastp = last_shot_status['shot']
          if last_shot_status['is_sunk']:
            self.map[lastp.x][lastp.y] = 'S'
          elif last_shot_status['is_hit']:
            self.map[lastp.x][lastp.y] = 'H'
          else:
            self.map[lastp.x][lastp.y] = 'M'

        p = self.get_best_shot()

        self.my_shots.append(p)
        self.seenX[p.x] += 1
        self.seenY[p.y] += 1

        return p
