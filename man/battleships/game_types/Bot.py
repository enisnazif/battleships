from abc import abstractmethod
from man.battleships.game_types import Ship, Point, Orientation
from typing import List, Tuple


# TODO: A bot should not own its board!


class Bot:
    def __init__(self):
        self._last_shot_status = (None, None)

    @property
    def name(self):
        return str(type(self).__name__)

    @property
    def last_shot_status(self):
        return self._last_shot_status

    @last_shot_status.setter
    def last_shot_status(self, value):
        self._last_shot_status = value

    @abstractmethod
    def get_ship_placements(
            self, ships: List[Ship]
    ) -> List[Tuple[Ship, Point, Orientation]]:
        """ This method should return a valid ship placement on the board of the opponent. It is called once """
        pass

    @abstractmethod
    def get_shot(self) -> Point:
        """ This method should return a valid shot on the board as an (x,y) coordinate. It is called by the game engine each round """
        pass
