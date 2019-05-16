import random
from typing import List, Dict, Union, Tuple

from config import BOARD_SIZE
from game_types import Bot, Board, Point, Ship, ShipType, Orientation

from collections import namedtuple

# state empty, missed, hit, sunk

cell_state = namedtuple('cellstate', ['point', 'state'])


class Team1Bot(Bot):
    """ Hello! I am a dumb sample bot who places its ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.cell_states = [[]]
        self.hits = []
        self.misses = []

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
        last_shot_status = self.last_shot_status

        # Example response:

        # {
        #    'shot': Point(4, 5),                                # type: Point
        #    'is_hit': True,                                     # type: bool
        #    'is_sunk' True,                                     # type: bool
        #    'ship_sunk': <ShipType.Battleship: 'Battleship'>,   # type: ShipType
        #    'error': None                                       # type: Union[None, Exception]
        # }

        # last_shot_status(self, value: Dict[str, Union[Point, bool, ShipType, None]]):
        last_shot_status = self.last_shot_status

        last_shot = last_shot_status['shot']
        is_hit = last_shot_status['is_hit']
        is_sunk = last_shot_status['is_sunk']
        is_error = last_shot_status['error']
        ship_sunk = last_shot_status['ship_sunk']

        first_shot = last_shot is not None
        previous_hit = None if not len(self.hits) else self.hits[-1]
        if is_hit:
            self.hits.append(last_shot)
            if previous_hit:
                if previous_hit.x == last_shot.x:
                    for dy in [-1, 1]:
                        yy = max(0, min(previous_hit.y + dy, BOARD_SIZE-1))
                        point = Point(previous_hit.x, yy)
                        if point not in self.my_shots:
                            self.my_shots.append(point)
                            return point
                if previous_hit.y == last_shot.y:
                    for dx in [-1, 1]:
                        xx = max(0, min(previous_hit.x + dx, BOARD_SIZE-1))
                        point = Point(xx, previous_hit.y)
                        if point not in self.my_shots:
                            self.my_shots.append(point)
                            return point

            if not is_sunk:
                for dx in [-1, 1]:
                    for dy in [-1, 1]:
                        xx = last_shot.x+dx
                        yy = last_shot.y+dy
                        xx = max(0, min(xx, BOARD_SIZE-1))
                        yy = max(0, min(yy, BOARD_SIZE-1))
                        point = Point(xx, yy)
                        if point not in self.my_shots:
                            self.my_shots.append(point)
                            return point
        else:
            self.misses.append(last_shot)

        if is_error:
            print('error', is_error)

        x = random.randrange(0, BOARD_SIZE)
        y = random.randrange(0, BOARD_SIZE)

        while Point(x, y) in self.my_shots:
            x = random.randrange(0, BOARD_SIZE)
            y = random.randrange(0, BOARD_SIZE)

        self.my_shots.append(Point(x, y))
        return Point(x, y)
        if is_sunk:
            pass
        if ship_sunk:
            pass

    def initial_case():
        pass
