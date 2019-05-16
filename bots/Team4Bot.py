import random
from typing import List, Dict, Union, Tuple

from config import BOARD_SIZE
from game_types import Bot, Board, Point, Ship, ShipType, Orientation


def _adjancent_points(p):
    points = [
        Point(x=p.x, y=p.y+1),
        Point(x=p.x, y=p.y-1),
        Point(x=p.x+1, y=p.y),
        Point(x=p.x-1, y=p.y),
    ]
    return [p for p in points if 0 <= p.x < BOARD_SIZE and 0 <= p.y < BOARD_SIZE]

class Team4Bot(Bot):
    """ Hello! I am a dumb sample bot who places its ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.next_steps = []
        self.shots = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if ((x % 2) == 0 and (y % 2) == 1) or ((x % 2) == 1 and (y % 2) == 0):
                    self.shots.append(Point(x=x, y=y))

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
        next_shot = None
        if self.last_shot_status['is_hit'] and not self.last_shot_status['is_sunk']:
             self.next_steps.extend(_adjancent_points(self.last_shot_status['shot']))
        
        if self.next_steps:
            try:
                next_shot = self.next_steps.pop()
                while next_shot in self.my_shots:
                    next_shot = self.next_steps.pop()
            except IndexError:
                next_shot = None
        
        if next_shot is not None:
            self.my_shots.append(next_shot)
            return next_shot
        else:
            next_shot = random.choice(self.shots)
            while next_shot in self.my_shots:
                next_shot = random.choice(self.shots)
            
    
            self.my_shots.append(next_shot)

            return next_shot
